import React, { useState, useEffect, useRef, useCallback } from 'react'
import useSWR, { mutate } from 'swr'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, BarChart, Bar, Cell, PieChart, Pie, Legend
} from 'recharts'
import './App.css'

const API = ''  // Use relative URLs — nginx proxies /api/ to backend, works from any host

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const fetcher = url => fetch(url).then(r => r.ok ? r.json() : Promise.reject(r.statusText))

function useFetch(url, deps = []) {
  // We use the URL as the SWR key. SWR handles the caching and deps implicitly by the key.
  const { data, error, isValidating } = useSWR(url ? url : null, fetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 2000,
    revalidateIfStale: true
  })
  return { data, loading: isValidating && !data, error, mutate }
}

function fmt(val, decimals = 2) {
  if (val === null || val === undefined) return '—'
  if (typeof val === 'object') return 'obj'
  return Number(val).toFixed(decimals)
}

function fmtZAR(val) {
  if (val === null || val === undefined) return '—'
  const n = Number(val)
  const abs = Math.abs(n).toLocaleString('en-ZA', { maximumFractionDigits: 0 })
  return (n >= 0 ? '+R ' : '-R ') + abs
}

function fmtPct(val) {
  if (val === null || val === undefined) return '—'
  const n = Number(val) * 100
  return (n >= 0 ? '+' : '') + n.toFixed(1) + '%'
}

function colorByVal(val, invert = false) {
  if (val === null || val === undefined) return 'var(--text-secondary)'
  const pos = invert ? val < 0 : val > 0
  return pos ? 'var(--success)' : 'var(--critical)'
}

function statusColor(s) {
  return { PASS: '#00ff88', FAIL: '#ff4444', REVIEW: '#ffcc00', PENDING: '#a0a0a0' }[s] || '#a0a0a0'
}

function statusBg(s) {
  return { PASS: 'rgba(0,255,136,0.1)', FAIL: 'rgba(255,68,68,0.12)', REVIEW: 'rgba(255,204,0,0.1)', PENDING: 'rgba(160,160,160,0.08)' }[s] || 'transparent'
}

function winRateColor(wr) {
  if (wr === null || wr === undefined) return 'var(--text-secondary)'
  const pct = wr * 100
  if (pct >= 85) return 'var(--success)'
  if (pct >= 70) return 'var(--warning)'
  return 'var(--critical)'
}

function fmtDuration(seconds) {
  if (!seconds) return '—'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  if (h > 0) return `${h}h ${m}m`
  return `${m}m`
}

// Parse a naive timestamp string from the API (stored as UTC in Docker) as UTC,
// so the browser displays it in local SAST time.
function toLocalTime(ts) {
  if (!ts) return null
  const s = String(ts)
  const hastz = s.endsWith('Z') || /[+-]\d{2}:\d{2}$/.test(s)
  return new Date(hastz ? s : s.replace(' ', 'T') + 'Z')
}

// ---------------------------------------------------------------------------
// KPI Card
// ---------------------------------------------------------------------------

function KpiCard({ label, value, delta, deltaPositive, unit, accent }) {
  return (
    <div className="kpi-card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value" style={{ color: accent || 'var(--text-primary)' }}>
        {typeof value === 'object' ? 'err' : (value ?? <span style={{ color: 'var(--text-secondary)' }}>—</span>)}
      </div>
      {delta && (
        <div className="kpi-delta" style={{ color: deltaPositive ? 'var(--success)' : 'var(--critical)' }}>
          {deltaPositive ? '↑' : '↓'} {delta}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Equity Chart
// ---------------------------------------------------------------------------

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="chart-tooltip">
      <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color, fontSize: '0.8rem' }}>
          {p.name}: {p.name === 'equity' ? fmtZAR(p.value) : fmtZAR(p.value)}
        </div>
      ))}
    </div>
  )
}

function SignalTypePill({ type }) {
  const isBuy = type === 'BUY'
  return (
    <span style={{
      padding: '0.15rem 0.4rem', borderRadius: 4, fontSize: '0.7rem', fontWeight: 700,
      background: isBuy ? 'rgba(0,255,136,0.1)' : 'rgba(255,68,68,0.1)',
      color: isBuy ? 'var(--success)' : 'var(--critical)',
      border: `1px solid ${isBuy ? 'rgba(0,255,136,0.2)' : 'rgba(255,68,68,0.2)'}`
    }}>
      {type}
    </span>
  )
}

function EquityChart({ lookbackDays }) {
  const { data, loading, error } = useFetch(`${API}/api/analytics/daily?lookback_days=${lookbackDays}`, [lookbackDays])

  const chartData = React.useMemo(() => {
    if (!data?.daily) return []
    const daily = data.daily

    // Handle both list-of-dicts and dict formats
    let entries = []
    if (Array.isArray(daily)) {
      entries = daily
    } else if (typeof daily === 'object') {
      entries = Object.entries(daily).map(([date, val]) => ({
        date,
        ...(typeof val === 'object' ? val : { pnl: val })
      }))
    }

    // Sort by date and build cumulative equity
    entries.sort((a, b) => new Date(a.date) - new Date(b.date))

    let cumulative = 0
    return entries.map(e => {
      const pnl = Number(e.pnl || e.net_profit || e.profit || 0)
      cumulative += pnl
      return {
        date: e.date ? String(e.date).slice(5) : '',   // MM-DD
        pnl: pnl,
        equity: cumulative,
      }
    })
  }, [data])

  if (loading) return <div className="chart-placeholder">Loading equity curve...</div>
  if (error) return <div className="chart-placeholder error">Could not load equity data</div>
  if (!chartData.length) return <div className="chart-placeholder">No trade data in the selected period</div>

  const minVal = Math.min(...chartData.map(d => d.equity))
  const domain = [Math.min(0, minVal * 1.05), 'auto']

  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={chartData} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="equityGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.25} />
            <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="negGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="var(--critical)" stopOpacity={0.2} />
            <stop offset="95%" stopColor="var(--critical)" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis dataKey="date" tick={{ fill: '#a0a0a0', fontSize: 10 }} axisLine={false} tickLine={false} interval="preserveStartEnd" />
        <YAxis
          tick={{ fill: '#a0a0a0', fontSize: 10 }}
          axisLine={false}
          tickLine={false}
          width={60}
          tickFormatter={v => `R${(v / 1000).toFixed(0)}k`}
          domain={domain}
        />
        <Tooltip content={<CustomTooltip />} />
        <Area
          type="monotone"
          dataKey="equity"
          name="equity"
          stroke="var(--accent-primary)"
          strokeWidth={2}
          fill="url(#equityGrad)"
          dot={false}
          activeDot={{ r: 4, fill: 'var(--accent-primary)', strokeWidth: 0 }}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

// ---------------------------------------------------------------------------
// Daily P&L Bar Chart
// ---------------------------------------------------------------------------

function DailyPnlChart({ lookbackDays }) {
  const { data, loading } = useFetch(`${API}/api/analytics/daily?lookback_days=${lookbackDays}`, [lookbackDays])

  const chartData = React.useMemo(() => {
    if (!data?.daily) return []
    const daily = data.daily
    let entries = Array.isArray(daily)
      ? daily
      : Object.entries(daily).map(([date, val]) => ({ date, ...(typeof val === 'object' ? val : { pnl: val }) }))
    entries.sort((a, b) => new Date(a.date) - new Date(b.date))
    return entries.slice(-30).map(e => ({
      date: e.date ? String(e.date).slice(5) : '',
      pnl: Number(e.pnl || e.net_profit || e.profit || 0)
    }))
  }, [data])

  if (loading) return <div className="chart-placeholder" style={{ height: 100 }}>Loading...</div>
  if (!chartData.length) return <div className="chart-placeholder" style={{ height: 100 }}>No data</div>

  return (
    <ResponsiveContainer width="100%" height={100}>
      <BarChart data={chartData} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
        <XAxis dataKey="date" tick={{ fill: '#a0a0a0', fontSize: 9 }} axisLine={false} tickLine={false} interval={4} />
        <Tooltip
          formatter={(val) => [fmtZAR(val), 'Daily P&L']}
          contentStyle={{ background: '#0b0e14', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 6, fontSize: 11 }}
          labelStyle={{ color: '#a0a0a0' }}
        />
        <Bar dataKey="pnl" radius={[2, 2, 0, 0]}>
          {chartData.map((entry, index) => (
            <Cell key={index} fill={entry.pnl >= 0 ? 'var(--success)' : 'var(--critical)'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

// ---------------------------------------------------------------------------
// KPI Strip — Feature 1
// ---------------------------------------------------------------------------

function KpiStrip({ lookbackDays }) {
  const { data, loading } = useFetch(`${API}/api/analytics/summary?lookback_days=${lookbackDays}`, [lookbackDays])
  const s = data?.account_summary

  const cards = [
    {
      label: `Net P&L (${lookbackDays}d)`,
      value: s ? fmtZAR(s.net_profit) : loading ? '...' : '—',
      accent: s ? colorByVal(s.net_profit) : undefined,
      delta: s ? `ROI ${fmtPct(s.roi_pct)}` : undefined,
      deltaPositive: s?.roi_pct > 0
    },
    {
      label: 'Win Rate',
      value: s ? fmt(s.win_rate * 100, 1) + '%' : loading ? '...' : '—',
      accent: s ? winRateColor(s.win_rate) : undefined,
      delta: s ? `${s.winning_trades}W / ${s.losing_trades}L` : undefined,
      deltaPositive: true
    },
    {
      label: 'Sharpe Ratio',
      value: s ? fmt(s.sharpe_ratio) : loading ? '...' : '—',
      accent: s ? (s.sharpe_ratio >= 0.8 ? 'var(--success)' : 'var(--warning)') : undefined,
      delta: s ? (s.sharpe_ratio >= 0.8 ? '≥ 0.8 target ✓' : '< 0.8 target ✗') : undefined,
      deltaPositive: s?.sharpe_ratio >= 0.8
    },
    {
      label: 'Max Drawdown',
      value: s ? fmt(s.max_drawdown_pct * 100, 1) + '%' : loading ? '...' : '—',
      accent: s ? (Math.abs(s.max_drawdown_pct) < 0.12 ? 'var(--warning)' : 'var(--critical)') : undefined,
      delta: s ? (Math.abs(s.max_drawdown_pct) < 0.12 ? '< 12% limit ✓' : '> 12% limit ✗') : undefined,
      deltaPositive: s ? Math.abs(s.max_drawdown_pct) < 0.12 : false
    },
    {
      label: 'Profit Factor',
      value: s ? fmt(s.profit_factor) : loading ? '...' : '—',
      accent: s ? (s.profit_factor >= 1.5 ? 'var(--success)' : 'var(--warning)') : undefined,
      delta: s ? `RR ${fmt(s.risk_reward_ratio)}` : undefined,
      deltaPositive: s?.profit_factor >= 1.5
    },
    {
      label: 'Total Trades',
      value: s ? s.total_trades : loading ? '...' : '—',
      accent: 'var(--accent-primary)',
      delta: s ? `${fmt(s.avg_win / (s.avg_loss || 1), 2)}x avg W/L` : undefined,
      deltaPositive: true
    }
  ]

  return (
    <div className="kpi-strip">
      {cards.map((c, i) => <KpiCard key={i} {...c} />)}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Strategy Performance Table — Feature 2
// ---------------------------------------------------------------------------

function StrategyTable({ lookbackDays }) {
  const { data, loading, error } = useFetch(`${API}/api/analytics/by-strategy?lookback_days=${lookbackDays}`, [lookbackDays])
  const { data: configData } = useFetch(`${API}/api/config/active`, [])
  
  const [sortKey, setSortKey] = useState('net_profit')
  const [sortDir, setSortDir] = useState('desc')

  const activeSlugs = React.useMemo(() => {
    if (!configData?.strategies) return new Set()
    return new Set(configData.strategies.map(s => s.name.toLowerCase().replace(/ /g, '_')))
  }, [configData])

  const rows = React.useMemo(() => {
    if (!data?.strategies) return []
    return Object.entries(data.strategies).map(([name, m]) => ({ 
      name, 
      isActive: activeSlugs.has(name.toLowerCase().replace(/ /g, '_')),
      ...m 
    }))
  }, [data, activeSlugs])

  const sorted = React.useMemo(() => {
    return [...rows].sort((a, b) => {
      const av = a[sortKey] ?? -Infinity
      const bv = b[sortKey] ?? -Infinity
      return sortDir === 'desc' ? bv - av : av - bv
    })
  }, [rows, sortKey, sortDir])

  function handleSort(key) {
    if (sortKey === key) setSortDir(d => d === 'desc' ? 'asc' : 'desc')
    else { setSortKey(key); setSortDir('desc') }
  }

  function SortTh({ label, field }) {
    const active = sortKey === field
    return (
      <th onClick={() => handleSort(field)} className="sortable-th">
        {label} {active ? (sortDir === 'desc' ? '↓' : '↑') : <span style={{ opacity: 0.3 }}>↕</span>}
      </th>
    )
  }

  if (loading && !data) return <div className="table-placeholder">Loading strategy metrics...</div>
  if (error) return <div className="table-placeholder error">Analytics API unavailable — start the backend server</div>
  if (!sorted.length) return <div className="table-placeholder">No trade data for this period. Trades will appear as the bot runs.</div>

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Strategy</th>
            <SortTh label="Trades" field="total_trades" />
            <SortTh label="Win Rate" field="win_rate" />
            <SortTh label="Sharpe" field="sharpe_ratio" />
            <SortTh label="Prof. Factor" field="profit_factor" />
            <SortTh label="Max DD" field="max_drawdown_pct" />
            <SortTh label="Net P&L" field="net_profit" />
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map(s => {
            const passed = s.win_rate >= 0.9 && s.sharpe_ratio >= 0.8 && Math.abs(s.max_drawdown_pct || 0) < 0.12
            const failed = s.win_rate < 0.65 || s.sharpe_ratio < 0.5 || Math.abs(s.max_drawdown_pct || 0) >= 0.15
            const rowStatus = passed ? 'PASS' : failed ? 'FAIL' : 'REVIEW'

            return (
              <tr key={s.name} className="data-row">
                <td className="strat-name">
                   <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {s.name.replace(/_/g, ' ')}
                      {s.isActive && <span className="status-badge" style={{ fontSize: '0.6rem', padding: '2px 4px', background: 'rgba(0,230,118,0.1)', color: '#00e676', borderColor: 'rgba(0,230,118,0.2)' }}>ACTIVE</span>}
                   </div>
                </td>
                <td>{s.total_trades ?? '—'}</td>
                <td style={{ color: winRateColor(s.win_rate), fontWeight: 600 }}>
                  {s.win_rate != null ? fmt(s.win_rate * 100, 1) + '%' : '—'}
                </td>
                <td style={{ color: s.sharpe_ratio >= 0.8 ? 'var(--success)' : 'var(--warning)' }}>
                  {fmt(s.sharpe_ratio)}
                </td>
                <td style={{ color: s.profit_factor >= 1.5 ? 'var(--success)' : 'var(--text-secondary)' }}>
                  {fmt(s.profit_factor)}
                </td>
                <td style={{ color: Math.abs(s.max_drawdown_pct || 0) >= 0.12 ? 'var(--critical)' : 'var(--warning)' }}>
                  {s.max_drawdown_pct != null ? fmt(s.max_drawdown_pct * 100, 1) + '%' : '—'}
                </td>
                <td style={{ color: colorByVal(s.net_profit), fontWeight: 600 }}>
                  {fmtZAR(s.net_profit)}
                </td>
                <td>
                  <span className="status-pill" style={{ color: statusColor(rowStatus), background: statusBg(rowStatus) }}>
                    {rowStatus}
                  </span>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Backtest Run History Table — Feature 3
// ---------------------------------------------------------------------------

function BacktestTable() {
  const [filter, setFilter] = useState({ 
    strategy: '', 
    status: '',
    winRateMin: '',
    sharpeMin: '',
    pfMin: '',
    profitMin: '',
    ddMax: ''
  })
  const [applied, setApplied] = useState({ 
    strategy: '', 
    status: '',
    winRateMin: '',
    sharpeMin: '',
    pfMin: '',
    profitMin: '',
    ddMax: ''
  })

  const url = React.useMemo(() => {
    const p = new URLSearchParams({ limit: '100' })
    if (applied.strategy) p.set('strategy', applied.strategy)
    if (applied.status) p.set('status', applied.status)
    if (applied.winRateMin) p.set('win_rate_min', Number(applied.winRateMin) / 100)
    if (applied.sharpeMin) p.set('sharpe_min', applied.sharpeMin)
    if (applied.pfMin) p.set('pf_min', applied.pfMin)
    if (applied.profitMin) p.set('profit_min', applied.profitMin)
    if (applied.ddMax) p.set('dd_max', Number(applied.ddMax) / 100)
    return `${API}/api/backtests?${p}`
  }, [applied])

  // Auto-refresh every 60 s
  const [btRefreshKey, setBtRefreshKey] = React.useState(0)
  const [btLastSync, setBtLastSync] = React.useState(null)
  React.useEffect(() => {
    const id = setInterval(() => {
      setBtRefreshKey(k => k + 1)
      setBtLastSync(new Date())
    }, 60000)
    return () => clearInterval(id)
  }, [])

  const { data, loading, error } = useFetch(url, [url, btRefreshKey])
  const { data: stats } = useFetch(`${API}/api/backtests/stats/summary`, [btRefreshKey])

  const [restoring, setRestoring] = useState(null)
  const [restoreData, setRestoreData] = useState(null)

  async function handleRestore(runId) {
    setRestoring(runId)
    try {
      const r = await fetch(`${API}/api/backtests/${runId}/restore`)
      const d = await r.json()
      setRestoreData(d)
    } catch (e) {
      alert('Restore failed: ' + e)
    }
    setRestoring(null)
  }

  const runs = data?.runs || []

  return (
    <div>
      {/* Summary row */}
      {stats && (
        <div className="bt-stats-row">
          <div className="bt-stat">
            <span className="bt-stat-n">{stats.total_runs ?? 0}</span>
            <span className="bt-stat-l">Total Runs</span>
          </div>
          <div className="bt-stat">
            <span className="bt-stat-n" style={{ color: 'var(--success)' }}>{stats.pass_count ?? 0}</span>
            <span className="bt-stat-l">Passed</span>
          </div>
          <div className="bt-stat">
            <span className="bt-stat-n" style={{ color: 'var(--warning)' }}>{stats.review_count ?? 0}</span>
            <span className="bt-stat-l">Review</span>
          </div>
          <div className="bt-stat">
            <span className="bt-stat-n" style={{ color: 'var(--critical)' }}>{stats.fail_count ?? 0}</span>
            <span className="bt-stat-l">Failed</span>
          </div>
          <div className="bt-stat">
            <span className="bt-stat-n" style={{ color: 'var(--accent-primary)' }}>{stats.unique_strategies ?? 0}</span>
            <span className="bt-stat-l">Strategies</span>
          </div>
          {stats.best_net_profit_zar != null && (
            <div className="bt-stat">
              <span className="bt-stat-n" style={{ color: 'var(--success)' }}>{fmtZAR(stats.best_net_profit_zar)}</span>
              <span className="bt-stat-l">Best Run</span>
            </div>
          )}
        </div>
      )}

      {/* Filters */}
      <div className="bt-filters" style={{ flexWrap: 'wrap', gap: '0.75rem' }}>
        <input
          className="bt-input"
          placeholder="Strategy..."
          value={filter.strategy}
          onChange={e => setFilter(f => ({ ...f, strategy: e.target.value }))}
          onKeyDown={e => e.key === 'Enter' && setApplied(filter)}
          style={{ width: 140 }}
        />
        <select className="bt-select" value={filter.status} onChange={e => { 
          const newF = { ...filter, status: e.target.value };
          setFilter(newF); 
          setApplied(newF);
        }}>
          <option value="">All statuses</option>
          <option value="PASS">PASS</option>
          <option value="REVIEW">REVIEW</option>
          <option value="FAIL">FAIL</option>
        </select>
        
        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>WR% {'>'}</span>
          <input className="bt-input" type="number" placeholder="0" value={filter.winRateMin} 
            onChange={e => setFilter(f => ({...f, winRateMin: e.target.value}))} style={{ width: 50 }} />
        </div>
        
        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Sharpe {'>'}</span>
          <input className="bt-input" type="number" step="0.1" placeholder="0" value={filter.sharpeMin} 
            onChange={e => setFilter(f => ({...f, sharpeMin: e.target.value}))} style={{ width: 50 }} />
        </div>

        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>PF {'>'}</span>
          <input className="bt-input" type="number" step="0.1" placeholder="0" value={filter.pfMin} 
            onChange={e => setFilter(f => ({...f, pfMin: e.target.value}))} style={{ width: 50 }} />
        </div>

        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>DD% {'<'}</span>
          <input className="bt-input" type="number" step="1" placeholder="100" value={filter.ddMax} 
            onChange={e => setFilter(f => ({...f, ddMax: e.target.value}))} style={{ width: 50 }} />
        </div>

        <button className="bt-btn" onClick={() => setApplied(filter)}>Apply</button>
        <button className="bt-btn secondary" onClick={() => { 
          const empty = { strategy: '', status: '', winRateMin: '', sharpeMin: '', pfMin: '', profitMin: '', ddMax: '' };
          setFilter(empty); 
          setApplied(empty); 
        }}>Clear</button>
        
        <span style={{ marginLeft: 'auto', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          {data?.total ?? 0} runs
          {btLastSync && <span style={{ marginLeft: 12, opacity: 0.7 }}>&middot; synced {btLastSync.toLocaleTimeString()}</span>}
        </span>
      </div>

      {loading && <div className="table-placeholder">Loading backtest history...</div>}
      {error && <div className="table-placeholder error">Backtest API unavailable. Run the DB migration first:<br /><code>psql -d trading_platform -f scripts/migrate_backtest_runs.sql</code></div>}

      {!loading && !error && (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Run ID</th>
                <th>Strategy</th>
                <th>Run Date</th>
                <th>Period</th>
                <th>Win Rate</th>
                <th>Sharpe</th>
                <th>Prof. Factor</th>
                <th>Max DD</th>
                <th>Net P&L</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {runs.length === 0 && (
                <tr><td colSpan={11} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  No backtest runs yet. Runs are logged automatically when you execute a backtest.
                </td></tr>
              )}
              {runs.map(r => (
                <tr key={r.run_id} className="data-row">
                  <td><span className="run-id-cell">{r.run_id}</span></td>
                  <td className="strat-name">{r.strategy_name?.replace(/_/g, ' ')}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                    {r.run_date ? toLocalTime(r.run_date)?.toLocaleDateString() ?? '—' : '—'}
                  </td>
                  <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                    {r.period_start && r.period_end
                      ? `${r.period_start} → ${r.period_end}`
                      : '—'}
                  </td>
                  <td style={{ color: winRateColor(r.win_rate), fontWeight: 600 }}>
                    {r.win_rate != null ? fmt(r.win_rate * 100, 1) + '%' : '—'}
                  </td>
                  <td style={{ color: (r.sharpe_ratio ?? 0) >= 0.8 ? 'var(--success)' : 'var(--warning)' }}>
                    {fmt(r.sharpe_ratio)}
                  </td>
                  <td>{fmt(r.profit_factor)}</td>
                  <td style={{ color: Math.abs(r.max_drawdown_pct ?? 0) >= 0.12 ? 'var(--critical)' : 'var(--warning)' }}>
                    {r.max_drawdown_pct != null ? fmt(r.max_drawdown_pct * 100, 1) + '%' : '—'}
                  </td>
                  <td style={{ color: colorByVal(r.net_profit_zar), fontWeight: 600 }}>
                    {fmtZAR(r.net_profit_zar)}
                  </td>
                  <td>
                    <span className="status-pill" style={{ color: statusColor(r.status), background: statusBg(r.status) }}>
                      {r.status}
                    </span>
                  </td>
                  <td>
                    <button
                      className="restore-btn"
                      onClick={() => handleRestore(r.run_id)}
                      disabled={restoring === r.run_id}
                    >
                      {restoring === r.run_id ? '...' : 'Restore'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Restore detail panel */}
      {restoreData && (
        <div className="restore-panel">
          <div className="restore-header">
            <span>Snapshot: <strong style={{ color: 'var(--accent-primary)' }}>{restoreData.run_id}</strong> — {restoreData.strategy_name}</span>
            <button className="restore-close" onClick={() => setRestoreData(null)}>✕</button>
          </div>
          <div className="restore-body">
            <div className="restore-col">
              <h4>Strategy Parameters</h4>
              <pre className="restore-pre">{JSON.stringify(restoreData.params || {}, null, 2)}</pre>
            </div>
            <div className="restore-col">
              <h4>Run Summary</h4>
              <div className="restore-metrics">
                {Object.entries(restoreData.summary || {}).filter(([k, v]) => v !== null).map(([k, v]) => (
                  <div key={k} className="restore-metric-row">
                    <span className="restore-metric-key">{k.replace(/_/g, ' ')}</span>
                    <span className="restore-metric-val">{typeof v === 'number' ? fmt(v) : String(v)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: 8 }}>
            Restored at {toLocalTime(restoreData.restored_at)?.toLocaleString() ?? '—'}
          </div>
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Strategy Intelligence Table — NEW
// ---------------------------------------------------------------------------

function StrategyIntelligenceTable() {
  const { data, loading } = usePolling(`${API}/api/intelligence/best-strategies`, 30000)

  if (loading && !data) return <div className="card">Loading Strategy Intelligence...</div>

  return (
    <div className="card intel-card" style={{ marginTop: '1rem', background: 'rgba(0, 242, 255, 0.01)' }}>
      <div className="card-head">
        <h3 className="card-h">Strategy Intelligence & Maturity</h3>
        <div className="status-badge" style={{ background: 'rgba(112, 0, 255, 0.1)', color: '#b08cff', border: '1px solid rgba(112, 0, 255, 0.2)' }}>
          AI Training Ready
        </div>
      </div>
      
      <div className="table-wrapper">
        <table className="intel-table" style={{ fontSize: '0.8rem' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>Strategy</th>
              <th style={{ textAlign: 'center' }}>Maturity</th>
              <th style={{ textAlign: 'center' }}>Profile</th>
              <th style={{ textAlign: 'right' }}>Sharpe</th>
              <th style={{ textAlign: 'right' }}>Win Rate</th>
              <th style={{ textAlign: 'left', paddingLeft: '1.5rem' }}>Latest Tweaks & Findings</th>
            </tr>
          </thead>
          <tbody>
            {data?.map((s, i) => (
              <tr key={i} className="intel-row">
                <td style={{ padding: '12px' }}>
                  <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{s.strategy.replace(/_/g, ' ')}</div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--accent-primary)' }}>{s.symbol} {s.timeframe}</div>
                </td>
                <td style={{ textAlign: 'center' }}>
                  <span className={`maturity-badge ${s.maturity > 5 ? 'maturity-high' : s.maturity > 2 ? 'maturity-mid' : 'maturity-low'}`}>
                    {s.maturity} Windows
                  </span>
                </td>
                <td style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', height: 40, gap: 3 }}>
                     <div className="histogram-bar" title={`Win Rate: ${s.win_rate}%`} style={{ height: `${Math.min(s.win_rate, 100)}%`, width: 6 }} />
                     <div className="histogram-bar" title={`Sharpe: ${s.sharpe}`} style={{ height: `${Math.min(s.sharpe * 20, 100)}%`, width: 6, background: 'var(--accent-secondary)' }} />
                     <div className="histogram-bar" title={`Maturity: ${s.maturity}`} style={{ height: `${Math.min(s.maturity * 10, 100)}%`, width: 6, background: '#7000ff' }} />
                </td>
                <td style={{ textAlign: 'right', fontWeight: 600, color: s.sharpe > 1.5 ? 'var(--success)' : 'var(--text-primary)' }}>{s.sharpe.toFixed(2)}</td>
                <td style={{ textAlign: 'right', fontWeight: 600 }}>{s.win_rate.toFixed(1)}%</td>
                <td style={{ paddingLeft: '1.5rem' }}>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 4 }}>
                    {s.tweaks?.slice(0, 3).map((t, ti) => (
                      <span key={ti} className="tweak-tag">{t}</span>
                    ))}
                  </div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)', fontStyle: 'italic' }}>
                    {s.findings?.slice(0, 60)}{s.findings?.length > 60 ? '...' : ''}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function ActivityFeed() {
  const { data, loading } = usePolling(`${API}/api/health/activity?limit=8`, 15000)

  if (loading && !data) return <div className="card">Loading Activity...</div>

  return (
    <div className="card" style={{ height: 'fit-content' }}>
      <div className="card-head">
        <h3 className="card-h">System Activity & Reports</h3>
        <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Scheduled Jobs</span>
      </div>
      <div className="activity-list" style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
        {data?.length === 0 && <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textAlign: 'center', padding: '1rem' }}>No recent activity.</div>}
        {data?.map((ev, i) => (
          <div key={i} className="activity-item" style={{ fontSize: '0.75rem', padding: '8px', background: 'rgba(255,255,255,0.02)', borderRadius: 6, borderLeft: `3px solid ${ev.status === 'SUCCESS' ? 'var(--success)' : ev.status === 'ERROR' ? 'var(--critical)' : 'var(--warning)'}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
              <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{ev.type.replace(/_/g, ' ')}</span>
              <span style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>{toLocalTime(ev.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
            <div style={{ color: 'var(--text-secondary)', lineHeight: '1.2' }}>{ev.message}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function SignalsMonitor() {
  const { data, loading } = usePolling(`${API}/api/papertrades/signals?limit=6`, 20000)

  if (loading && !data) return <div className="card">Loading Signals...</div>

  return (
    <div className="card">
      <div className="card-head">
        <h3 className="card-h">Live Signal Stream</h3>
        <div className="live-dot"><span className="pulse" />SCANNING</div>
      </div>
      <div style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {data?.signals?.length === 0 && <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textAlign: 'center', padding: '1rem' }}>Awaiting market opportunities...</div>}
        {data?.signals?.slice(0, 6).map((sig, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '8px', background: 'rgba(255,255,255,0.02)', borderRadius: 6 }}>
            <SignalTypePill type={sig.direction} />
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600, fontSize: '0.8rem' }}>{sig.pair} <span style={{ color: 'var(--text-secondary)', fontWeight: 400 }}>{sig.timeframe}</span></div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>{sig.strategy_name.replace(/_/g, ' ')}</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700 }}>{sig.price.toFixed(5)}</div>
              <div style={{ fontSize: '0.6rem', color: 'var(--text-secondary)' }}>{toLocalTime(sig.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function PerformanceDashboard({ lookbackDays }) {
  const { data, loading } = useFetch(`${API}/api/analytics/daily?lookback_days=${lookbackDays}`, [lookbackDays])
  const { data: summaryData } = useFetch(`${API}/api/analytics/summary?lookback_days=${lookbackDays}`, [lookbackDays])
  
  const days = React.useMemo(() => {
    if (!data?.daily) return []
    return [...data.daily].sort((a, b) => new Date(a.date) - new Date(b.date))
  }, [data])

  const s = summaryData?.account_summary

  if (loading) return <div className="table-placeholder">Loading performance data...</div>

  return (
    <div className="performance-view" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      
      {/* 1. Header Stats Grid */}
      <div className="stat-summary-grid">
         <div className="stat-item">
            <div className="stat-label">Total Net Profit</div>
            <div className="stat-value" style={{ color: colorByVal(s?.net_profit) }}>{fmtZAR(s?.net_profit)}</div>
         </div>
         <div className="stat-item">
            <div className="stat-label">Profit Factor</div>
            <div className="stat-value" style={{ color: (s?.profit_factor >= 2 ? 'var(--success)' : 'var(--text-primary)') }}>{fmt(s?.profit_factor)}</div>
         </div>
         <div className="stat-item">
            <div className="stat-label">Win Rate</div>
            <div className="stat-value" style={{ color: winRateColor(s?.win_rate) }}>{fmt(s?.win_rate * 100, 1)}%</div>
         </div>
         <div className="stat-item">
            <div className="stat-label">Recovery Factor</div>
            <div className="stat-value" style={{ color: 'var(--accent-primary)' }}>{fmt(s?.recovery_factor)}</div>
         </div>
         <div className="stat-item">
            <div className="stat-label">Avg Trade Duration</div>
            <div className="stat-value">{fmtDuration(s?.avg_duration_seconds)}</div>
         </div>
      </div>

      <div className="two-col" style={{ gridTemplateColumns: '2fr 1fr' }}>
        {/* 2. Trading Calendar */}
        <div className="card">
          <div className="calendar-header">
            <h3 className="card-h">Trading Calendar</h3>
            <div className="calendar-month-nav">
               <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>{new Date().toLocaleString('default', { month: 'long', year: 'numeric' })}</span>
            </div>
          </div>
          <div className="calendar-grid">
            {days.slice(-28).map(d => (
              <div key={d.date} className="calendar-day">
                <div className="calendar-date">{d.date.slice(8, 10)}</div>
                <div className="calendar-pnl" style={{ color: colorByVal(d.pnl) }}>
                  {d.pnl === 0 ? '—' : fmtZAR(d.pnl)}
                </div>
                <div className="calendar-pct" style={{ color: 'var(--text-secondary)' }}>
                  {d.trades > 0 ? `${d.trades} tr` : ''}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 3. Win Rate Radial / Breakdown */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <h3 className="card-h" style={{ alignSelf: 'flex-start', marginBottom: '2rem' }}>Win Probability</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Wins', value: s?.winning_trades || 1, fill: 'var(--success)' },
                  { name: 'Losses', value: s?.losing_trades || 1, fill: 'var(--critical)' }
                ]}
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                <Cell key="win" fill="var(--success)" />
                <Cell key="loss" fill="var(--critical)" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ textAlign: 'center', marginTop: '1rem' }}>
             <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--success)' }}>{fmt(s?.win_rate * 100, 1)}%</div>
             <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Weighted Win Rate</div>
          </div>
        </div>
      </div>

      {/* 4. Detailed Strategy Table (Reused) */}
      <div className="card">
         <div className="card-head">
            <h3 className="card-h">Strategy Performance Breakdown</h3>
         </div>
         <StrategyTable lookbackDays={lookbackDays} />
      </div>

    </div>
  )
}

function WfoIntelligencePanel() {
  const { data: status, loading: sLoading } = usePolling(`${API}/api/wfo/status`, 10000)
  const { data: alphas, loading: aLoading } = usePolling(`${API}/api/wfo/top-alphas`, 30000)

  if (sLoading && !status) return <div className="card" style={{ height: 200 }}>Analyzing WFO Stream...</div>

  return (
    <div className="wfo-intelligence">
      <div className="card" style={{ marginBottom: '1rem', borderLeft: '4px solid var(--accent-primary)' }}>
        <div className="card-head">
          <h3 className="card-h">Master WFO Sweep Status</h3>
          <div className="status-badge" style={{ 
            background: status?.is_active ? 'rgba(0, 230, 118, 0.1)' : 'rgba(255,255,255,0.05)',
            color: status?.is_active ? '#00e676' : 'var(--text-secondary)'
          }}>
            {status?.is_active && <div className="pulse" />}
            {status?.is_active ? 'Active Optimization' : 'Ready / Idle'}
          </div>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginTop: '0.5rem' }}>
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: 6 }}>
              <span style={{ color: 'var(--text-secondary)' }}>Strategy Progress</span>
              <span style={{ fontWeight: 700, color: 'var(--accent-primary)' }}>{status?.completed} / {status?.total}</span>
            </div>
            <div style={{ height: 8, background: 'rgba(255,255,255,0.05)', borderRadius: 4, overflow: 'hidden' }}>
              <div 
                style={{ 
                  height: '100%', 
                  background: 'linear-gradient(90deg, var(--accent-secondary), var(--accent-primary))',
                  width: `${status?.progress_pct}%`,
                  transition: 'width 1s ease-in-out'
                }} 
              />
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 800 }}>{status?.progress_pct}%</div>
            <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Completion</div>
          </div>
        </div>
      </div>

      <div className="two-col">
        <div className="card" style={{ background: 'rgba(0, 242, 255, 0.02)' }}>
          <div className="card-sub">Top Performing Alphas (OOS)</div>
          <div className="table-wrapper" style={{ border: 'none' }}>
            <table className="data-table" style={{ fontSize: '0.75rem' }}>
              <thead>
                <tr>
                  <th>Strategy</th>
                  <th>Symbol</th>
                  <th>Sharpe</th>
                  <th>Win Rate</th>
                </tr>
              </thead>
              <tbody>
                {alphas?.slice(0, 5).map((a, i) => (
                  <tr key={i} className="data-row">
                    <td style={{ fontWeight: 600 }}>{a.strategy.replace(/_/g, ' ')}</td>
                    <td style={{ color: 'var(--accent-primary)' }}>{a.symbol} {a.timeframe}</td>
                    <td style={{ color: a.avg_sharpe > 2 ? 'var(--success)' : 'inherit' }}>{a.avg_sharpe.toFixed(2)}</td>
                    <td>{a.avg_win_rate.toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="card-sub">Recent Sweep Results</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.5rem' }}>
            {status?.recent_results?.map((r, i) => (
              <div key={i} style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                fontSize: '0.75rem', 
                padding: '6px 8px', 
                background: 'rgba(255,255,255,0.02)',
                borderRadius: 6,
                borderLeft: `2px solid ${r.sharpe > 1.5 ? 'var(--success)' : 'var(--critical)'}`
              }}>
                <span>{r.strategy.slice(0, 15)}...</span>
                <span style={{ fontWeight: 600 }}>{r.sharpe.toFixed(1)} SR</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function usePolling(url, intervalMs) {
  const [data, setData] = React.useState(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState(null)
  const [lastSync, setLastSync] = React.useState(null)

  const fetchNow = React.useCallback(() => {
    fetch(url)
      .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
      .then(d => { setData(d); setError(null); setLastSync(new Date()); setLoading(false) })
      .catch(e => { setError(String(e)); setLoading(false) })
  }, [url])

  React.useEffect(() => {
    fetchNow()
    const id = setInterval(fetchNow, intervalMs)
    return () => clearInterval(id)
  }, [fetchNow, intervalMs])

  return { data, loading, error, lastSync, refetch: fetchNow }
}

// ---------------------------------------------------------------------------
// ConfigOverview – Summarized settings for every active strategy
// ---------------------------------------------------------------------------

function ConfigOverview() {
  const { data, loading } = useFetch(`${API}/api/config/active`, [])
  if (loading && !data) return <div className="card">Loading Strategy Configs...</div>
  if (!data?.strategies) return null

  return (
    <div className="card">
       <div className="card-head">
         <h3 className="card-h">Active Strategy Configs</h3>
         <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <span className="live-dot"><span className="pulse" /></span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{data.total_active} Active</span>
         </div>
       </div>
       <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
         {data.strategies.map(s => (
           <div key={s.slug} style={{ background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: 8, border: '1px solid rgba(255,255,255,0.05)', transition: 'transform 0.2s', cursor: 'default' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}>
             <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                <div>
                   <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-primary)' }}>{s.name}</div>
                   <div style={{ fontSize: '0.65rem', color: 'var(--accent-primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{s.category}</div>
                </div>
                <span className="status-pill" style={{ 
                   fontSize: '0.6rem', 
                   padding: '2px 6px',
                   background: s.tier === 'TIER_1' ? 'rgba(0,229,255,0.1)' : 'rgba(255,255,255,0.05)',
                   color: s.tier === 'TIER_1' ? 'var(--accent-primary)' : 'var(--text-secondary)',
                   border: `1px solid ${s.tier === 'TIER_1' ? 'rgba(0,229,255,0.2)' : 'rgba(255,255,255,0.1)'}`
                }}>{s.tier}</span>
             </div>
             <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: 10, display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {s.pairs.slice(0, 3).map(p => <span key={p} style={{ background: 'rgba(255,255,255,0.05)', padding: '1px 4px', borderRadius: 3 }}>{p}</span>)}
                {s.pairs.length > 3 && <span>+{s.pairs.length - 3} more</span>}
                <span style={{ marginLeft: 'auto', opacity: 0.7 }}>{s.timeframes.join(', ')}</span>
             </div>
             <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 12px', fontSize: '0.7rem', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: 8 }}>
                {Object.entries(s.parameters).slice(0, 4).map(([k,v]) => (
                  <div key={k} style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ opacity: 0.5 }}>{k.replace(/_/g, ' ')}:</span>
                    <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{typeof v === 'boolean' ? (v ? 'YES' : 'NO') : v}</span>
                  </div>
                ))}
             </div>
             <div style={{ marginTop: 10, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.65rem', color: s.mode === 'trade' ? 'var(--success)' : 'var(--warning)', fontWeight: 700 }}>
                   {s.mode.toUpperCase()} MODE
                </span>
                <span style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>Lot: {s.lot_size}</span>
             </div>
           </div>
         ))}
       </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// BacktestOvernightPanel — reads latest overnight JSON report (auto-sync 5 min)
// ---------------------------------------------------------------------------

function BacktestOvernightPanel() {
  const { data, loading, error, lastSync, refetch } =
    usePolling(`${API}/api/backtests/overnight/latest`, 5 * 60 * 1000)
  const [filter, setFilter] = React.useState('')
  const [statusFilter, setStatusFilter] = React.useState('')
  const [triggering, setTriggering] = React.useState(false)

  const results = React.useMemo(() => {
    if (!data?.results) return []
    return data.results.filter(r => {
      const nameMatch = !filter ||
        (r.strategy + ' ' + r.pair).toLowerCase().includes(filter.toLowerCase())
      const statMatch = !statusFilter || r.status === statusFilter
      return nameMatch && statMatch
    })
  }, [data, filter, statusFilter])

  const chartData = React.useMemo(() => {
    if (!data) return []
    return [
      { name: 'PASS', value: data.pass_count, fill: '#00ff88' },
      { name: 'REVIEW', value: data.review_count, fill: '#ffcc00' },
      { name: 'ERROR/SKIP', value: data.error_count, fill: '#ff4444' },
    ]
  }, [data])

  async function triggerBacktest() {
    setTriggering(true)
    try {
      const res = await fetch(`${API}/api/backtests/overnight/trigger?tier=1`, { method: 'POST' })
      const d = await res.json()
      alert(d.message || 'Backtest triggered')
    } catch (e) {
      alert('Trigger failed: ' + e)
    }
    setTriggering(false)
  }

  if (loading) return <div className="table-placeholder">Loading overnight report...</div>
  if (error) return (
    <div className="table-placeholder error">
      Overnight report not found &mdash; run the backtest first.<br />
      <button className="bt-btn" onClick={triggerBacktest} disabled={triggering}>
        {triggering ? 'Starting...' : 'Run Tier 1 Suite Now'}
      </button>
    </div>
  )

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem', marginBottom: '1rem' }}>
        {/* Visual Summary */}
        <div className="card" style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem' }}>
          <div className="card-sub" style={{ marginBottom: '1rem' }}>Status Distribution</div>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%" cy="50%"
                innerRadius={45}
                outerRadius={65}
                paddingAngle={5}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Stats and Controls */}
        <div>
          <div className="bt-stats-row" style={{ marginBottom: '0.75rem' }}>
            <div className="bt-stat">
              <span className="bt-stat-n">{data.total}</span>
              <span className="bt-stat-l">Total Combos</span>
            </div>
            <div className="bt-stat">
              <span className="bt-stat-n" style={{ color: 'var(--success)' }}>{data.pass_count}</span>
              <span className="bt-stat-l">PASS</span>
            </div>
            <div className="bt-stat">
              <span className="bt-stat-n" style={{ color: 'var(--warning)' }}>{data.review_count}</span>
              <span className="bt-stat-l">REVIEW</span>
            </div>
            <div style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
              <span>Report Date: {data.report_date}</span>
              {lastSync && <span style={{ opacity: 0.7 }}>Synced: {lastSync.toLocaleTimeString()}</span>}
              <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
                <button className="bt-btn secondary" style={{ padding: '4px 12px' }} onClick={refetch}>Refresh Data</button>
                <button className="bt-btn" style={{ padding: '4px 12px' }} onClick={triggerBacktest} disabled={triggering}>
                  {triggering ? 'Starting...' : 'Re-Run Suite'}
                </button>
              </div>
            </div>
          </div>

          <div className="bt-filters" style={{ marginBottom: '0.5rem', marginTop: '1.5rem' }}>
            <input className="bt-input" placeholder="Filter strategy / pair..."
              value={filter} onChange={e => setFilter(e.target.value)} />
            <select className="bt-select" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
              <option value="">All statuses</option>
              <option value="PASS">PASS</option>
              <option value="REVIEW">REVIEW</option>
            </select>
          </div>
        </div>
      </div>

      <div className="table-wrapper" style={{ maxHeight: '400px', overflowY: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Strategy</th><th>Pair</th><th>TF</th><th>Status</th>
              <th>WR%</th><th>Sharpe</th><th>MaxDD%</th><th>Trades</th><th>PF</th><th>Net P&L</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, i) => {
              const pnl = r.total_pnl ?? r.stats?.total_pnl
              const trades = r.total_trades ?? r.stats?.total_trades
              return (
                <tr key={i} className="data-row">
                  <td className="strat-name">{(r.strategy || '').replace(/_/g, ' ')}</td>
                  <td style={{ fontWeight: 600 }}>{r.pair}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>{r.timeframe}</td>
                  <td>
                    <span className="status-pill"
                      style={{ color: statusColor(r.status), background: statusBg(r.status) }}>
                      {r.status}
                    </span>
                  </td>
                  <td style={{ color: winRateColor(r.win_rate != null ? r.win_rate / 100 : null), fontWeight: 600 }}>
                    {r.win_rate != null ? r.win_rate.toFixed(1) + '%' : '—'}
                  </td>
                  <td style={{ color: (r.sharpe_ratio ?? 0) >= 0.8 ? 'var(--success)' : 'var(--warning)' }}>
                    {r.sharpe_ratio != null ? r.sharpe_ratio.toFixed(2) : '—'}
                  </td>
                  <td style={{ color: Math.abs(r.max_drawdown_pct ?? 0) >= 12 ? 'var(--critical)' : 'var(--text-secondary)' }}>
                    {r.max_drawdown_pct != null ? r.max_drawdown_pct.toFixed(1) + '%' : '—'}
                  </td>
                  <td>{trades ?? '—'}</td>
                  <td>{r.profit_factor != null ? r.profit_factor.toFixed(2) : '—'}</td>
                  <td style={{ color: colorByVal(pnl), fontWeight: 600 }}>
                    {pnl != null ? fmtZAR(pnl) : '—'}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// AutomationTab — Command Center for Backtests & Cleanup
// ---------------------------------------------------------------------------

function AutomationTab() {
  const { data: status, refetch: refetchStatus } = usePolling(`${API}/api/backtests/overnight/status`, 10000)
  const { data: runsData, refetch: refetchRuns } = usePolling(`${API}/api/backtests/overnight/runs?limit=10`, 30000)
  const [cleaning, setCleaning] = useState(false)
  const [triggering, setTriggering] = useState(false)

  async function handleCleanup() {
    if (!window.confirm('Archive reports older than 48 hours?')) return
    setCleaning(true)
    try {
      const res = await fetch(`${API}/api/backtests/overnight/cleanup`, { method: 'POST' })
      const d = await res.json()
      alert(`Cleanup successful! Archived ${d.archived_count} files.`)
      refetchRuns()
    } catch (e) {
      alert('Cleanup failed: ' + e)
    }
    setCleaning(false)
  }

  async function handleTrigger(tier) {
    setTriggering(true)
    try {
      const res = await fetch(`${API}/api/backtests/overnight/trigger?tier=${tier}`, { method: 'POST' })
      const d = await res.json()
      alert(d.message)
      refetchStatus()
    } catch (e) {
      alert('Trigger failed: ' + e)
    }
    setTriggering(false)
  }

  const runs = runsData?.runs || []

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Top row: Monitor + Commands */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        {/* Background Process Monitor */}
        <div className="card">
          <div className="card-head" style={{ marginBottom: '1.5rem' }}>
            <h3 className="card-h">System Monitor</h3>
            <div className="status-badge">
              <div className={`pulse ${!status?.running ? 'offline' : ''}`}
                   style={{ backgroundColor: status?.running ? 'var(--success)' : 'var(--text-secondary)' }} />
              {status?.running ? 'RUNNING' : 'IDLE'}
            </div>
          </div>

          {status?.running ? (
            <div style={{ padding: '1rem', background: 'rgba(0,255,136,0.05)', borderRadius: 8, border: '1px solid rgba(0,255,136,0.2)' }}>
              <div style={{ color: 'var(--success)', fontWeight: 600, marginBottom: 8 }}>Backtest in Progress...</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                Started: {toLocalTime(status.start_time)?.toLocaleString() ?? '—'}<br />
                PID: {status.pid}<br />
                Target: Tier 1 Suite
              </div>
              <div className="progress-bar" style={{ marginTop: 16 }}>
                <div className="progress-fill" style={{ width: '45%' }}></div>
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
              No active background tasks. Ready for commands.
            </div>
          )}
        </div>

        {/* Control Panel */}
        <div className="card">
          <div className="card-head" style={{ marginBottom: '1.5rem' }}>
            <h3 className="card-h">Automation Commands</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="command-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: 8 }}>
              <div>
                <div style={{ fontWeight: 600 }}>Overnight Validation (Tier 1)</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Run 76 combinations · Updates latest report</div>
              </div>
              <button className="bt-btn" onClick={() => handleTrigger(1)} disabled={triggering || status?.running}>
                {triggering ? 'Starting...' : 'Trigger Now'}
              </button>
            </div>

            <div className="command-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: 8 }}>
              <div>
                <div style={{ fontWeight: 600 }}>Report Management & Cleanup</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Archive data {'>'} 48h · Notifies Telegram on failure</div>
              </div>
              <button className="bt-btn secondary" onClick={handleCleanup} disabled={cleaning}>
                {cleaning ? 'Archiving...' : 'Run Cleanup'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Activity Log — full width */}
      <div className="card">
        <div className="card-head" style={{ marginBottom: '1.25rem' }}>
          <h3 className="card-h">Run Activity Log</h3>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', letterSpacing: '0.05em' }}>
            Last {runs.length} report{runs.length !== 1 ? 's' : ''} · auto-refresh 30s
          </div>
        </div>

        {runs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No reports found. Run a backtest to see activity here.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {/* Header row */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '160px 90px 90px 1fr 80px 80px 80px',
              gap: '0.75rem',
              padding: '0.4rem 0.75rem',
              fontSize: '0.7rem',
              color: 'var(--text-secondary)',
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              borderBottom: '1px solid rgba(255,255,255,0.06)'
            }}>
              <span>Timestamp</span>
              <span>Date</span>
              <span>Trigger</span>
              <span>Filename</span>
              <span style={{ textAlign: 'center', color: 'var(--success)' }}>PASS</span>
              <span style={{ textAlign: 'center', color: 'var(--warning)' }}>REVIEW</span>
              <span style={{ textAlign: 'center', color: 'var(--critical)' }}>ERRORS</span>
            </div>

            {runs.map((run, i) => {
              const isLatest = i === 0
              const passRate = run.total > 0 ? Math.round((run.pass_count / run.total) * 100) : 0
              const triggerColor = run.trigger === 'SCHEDULED' ? 'var(--accent)' : 'var(--text-secondary)'
              const triggerIcon = run.trigger === 'SCHEDULED' ? '⏱' : '▶'
              const genTime = run.generated
                ? toLocalTime(run.generated)?.toLocaleString('en-ZA', { dateStyle: 'short', timeStyle: 'short' }) ?? '—'
                : '—'

              return (
                <div key={run.filename} style={{
                  display: 'grid',
                  gridTemplateColumns: '160px 90px 90px 1fr 80px 80px 80px',
                  gap: '0.75rem',
                  alignItems: 'center',
                  padding: '0.6rem 0.75rem',
                  borderRadius: 6,
                  background: isLatest ? 'rgba(255,255,255,0.04)' : 'transparent',
                  border: isLatest ? '1px solid rgba(255,255,255,0.07)' : '1px solid transparent',
                  fontSize: '0.82rem',
                  transition: 'background 0.15s'
                }}>
                  <span style={{ color: isLatest ? 'var(--text-primary)' : 'var(--text-secondary)', fontFamily: 'monospace', fontSize: '0.78rem' }}>
                    {genTime}
                    {isLatest && <span style={{ marginLeft: 6, fontSize: '0.65rem', color: 'var(--accent)', fontFamily: 'sans-serif', letterSpacing: '0.05em' }}>LATEST</span>}
                  </span>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>{run.report_date}</span>
                  <span style={{ color: triggerColor, fontSize: '0.75rem', letterSpacing: '0.04em' }}>
                    {triggerIcon} {run.trigger}
                  </span>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.72rem', fontFamily: 'monospace', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {run.filename}
                  </span>
                  <span style={{ textAlign: 'center', color: 'var(--success)', fontWeight: 600 }}>
                    {run.pass_count}
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', fontWeight: 400, marginLeft: 2 }}>({passRate}%)</span>
                  </span>
                  <span style={{ textAlign: 'center', color: 'var(--warning)' }}>{run.review_count}</span>
                  <span style={{ textAlign: 'center', color: run.error_count > 0 ? 'var(--critical)' : 'var(--text-secondary)' }}>{run.error_count}</span>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// PaperTradeTab — live paper trading results, auto-sync every 30 s
// ---------------------------------------------------------------------------

function PaperTradeTab({ lookbackDays }) {
  const [ptDays, setPtDays] = React.useState(lookbackDays)
  const [tradeStatus, setTradeStatus] = React.useState('')
  const [sigHours, setSigHours] = React.useState(24)

  const summaryUrl = `${API}/api/papertrades/summary?lookback_days=${ptDays}`
  const tradesUrl  = `${API}/api/papertrades/trades?lookback_days=${ptDays}&limit=50` +
                     (tradeStatus ? `&status=${tradeStatus}` : '')
  const sigUrl     = `${API}/api/papertrades/signals?lookback_hours=${sigHours}&limit=100`

  const { data: summary, lastSync: sumSync, refetch: sumRefetch } = usePolling(summaryUrl, 30000)
  const { data: tradesData, lastSync: trSync, refetch: trRefetch } = usePolling(tradesUrl, 30000)
  const { data: sigData, lastSync: sigSync, refetch: sigRefetch } = usePolling(sigUrl, 30000)

  function refetchAll() { sumRefetch(); trRefetch(); sigRefetch() }

  const trades  = tradesData?.trades  || []
  const signals = sigData?.signals    || []

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: '1rem', flexWrap: 'wrap' }}>
        <select className="bt-select" value={ptDays} onChange={e => setPtDays(Number(e.target.value))}>
          <option value={1}>Last 24h</option>
          <option value={3}>Last 3 days</option>
          <option value={7}>Last 7 days</option>
          <option value={14}>Last 14 days</option>
          <option value={30}>Last 30 days</option>
        </select>
        <div className="status-badge" style={{ fontSize: '0.75rem' }}>
          <div className="pulse" style={{ backgroundColor: 'var(--success)' }} />
          Auto-sync 30s
        </div>
        {sumSync && <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Last: {sumSync.toLocaleTimeString()}</span>}
        <button className="bt-btn secondary" style={{ marginLeft: 'auto' }} onClick={refetchAll}>&#x21BB; Refresh Now</button>
      </div>

      {summary && !summary.error && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.75rem', marginBottom: '1.5rem' }}>
          <KpiCard label="Total Trades" value={summary.total_trades} />
          <KpiCard label="Win Rate"
            value={summary.win_rate != null ? summary.win_rate.toFixed(1) + '%' : '—'}
            accent={summary.win_rate >= 60 ? 'var(--success)' : summary.win_rate >= 45 ? 'var(--warning)' : 'var(--critical)'} />
          <KpiCard label="Net P&L (ZAR)" value={fmtZAR(summary.net_pnl_zar)} accent={colorByVal(summary.net_pnl_zar)} />
          <KpiCard label="Open Positions" value={summary.open_positions}
            accent={summary.open_positions > 0 ? 'var(--accent-primary)' : 'var(--text-secondary)'} />
          <KpiCard label="Signals (24h)" value={summary.signals_today} />
          <KpiCard label="Wins / Losses" value={`${summary.wins} / ${summary.losses}`} />
        </div>
      )}
      {summary?.error && (
        <div className="table-placeholder error" style={{ marginBottom: '1rem' }}>
          DB error: {summary.error} &mdash; is the paper engine running?
        </div>
      )}

      <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
        <div className="card-head" style={{ marginBottom: '0.75rem' }}>
          <h3 className="card-h">Paper Trades</h3>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <select className="bt-select" value={tradeStatus} onChange={e => setTradeStatus(e.target.value)}>
              <option value="">All</option>
              <option value="OPENED">Open only</option>
              <option value="CLOSED">Closed only</option>
            </select>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{trades.length} trades</span>
            {trSync && <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', opacity: 0.7 }}>{trSync.toLocaleTimeString()}</span>}
          </div>
        </div>
        <div className="table-wrapper" style={{ maxHeight: '300px', overflowY: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Strategy</th><th>Pair</th><th>Dir</th><th>Lots</th>
                <th>Entry</th><th>Exit</th><th>Open Time</th><th>P&L</th><th>Status</th>
              </tr>
            </thead>
            <tbody>
              {trades.length === 0 && (
                <tr><td colSpan={9} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  No paper trades in this window. Is the paper engine running?
                </td></tr>
              )}
              {trades.map((t, i) => (
                <tr key={i} className="data-row">
                  <td className="strat-name">{(t.strategy_name || '').replace(/_/g, ' ')}</td>
                  <td style={{ fontWeight: 600 }}>{t.pair}</td>
                  <td style={{ color: t.direction === 'BUY' ? 'var(--success)' : 'var(--critical)', fontWeight: 700 }}>
                    {t.direction}
                  </td>
                  <td style={{ fontSize: '0.78rem' }}>{t.lot_size != null ? t.lot_size.toFixed(2) : '—'}</td>
                  <td style={{ fontSize: '0.8rem' }}>{t.entry_price != null ? t.entry_price.toFixed(5) : '—'}</td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    {t.exit_price != null ? t.exit_price.toFixed(5) : '—'}
                  </td>
                  <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {t.open_time ? toLocalTime(t.open_time)?.toLocaleString() ?? '—' : '—'}
                  </td>
                  <td style={{ color: colorByVal(t.profit), fontWeight: 600 }}>
                    {t.profit != null ? fmtZAR(t.profit) : '—'}
                  </td>
                  <td>
                    <span className="status-pill" style={{
                      color: t.status === 'OPENED' ? 'var(--accent-primary)' :
                             (t.profit ?? 0) > 0 ? 'var(--success)' : 'var(--critical)',
                      background: t.status === 'OPENED' ? 'rgba(0,229,255,0.1)' :
                                  (t.profit ?? 0) > 0 ? 'rgba(0,255,136,0.1)' : 'rgba(255,68,68,0.1)'
                    }}>
                      {t.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card" style={{ padding: '1rem' }}>
        <div className="card-head" style={{ marginBottom: '0.75rem' }}>
          <h3 className="card-h">Recent Signals</h3>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <select className="bt-select" value={sigHours} onChange={e => setSigHours(Number(e.target.value))}>
              <option value={6}>Last 6h</option>
              <option value={24}>Last 24h</option>
              <option value={48}>Last 48h</option>
              <option value={168}>Last 7 days</option>
            </select>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{signals.length} signals</span>
            {sigSync && <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', opacity: 0.7 }}>{sigSync.toLocaleTimeString()}</span>}
          </div>
        </div>
        <div className="table-wrapper" style={{ maxHeight: '280px', overflowY: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Time</th><th>Strategy</th><th>Pair</th><th>TF</th>
                <th>Direction</th><th>Price</th><th>Validity</th><th>Taken</th>
              </tr>
            </thead>
            <tbody>
              {signals.length === 0 && (
                <tr><td colSpan={8} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  No signals in this window.
                </td></tr>
              )}
              {signals.map((s, i) => (
                <tr key={i} className="data-row">
                  <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {s.timestamp ? toLocalTime(s.timestamp)?.toLocaleString() ?? '—' : '—'}
                  </td>
                  <td className="strat-name">{(s.strategy_name || '').replace(/_/g, ' ')}</td>
                  <td style={{ fontWeight: 600 }}>{s.pair}</td>
                  <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{s.timeframe}</td>
                  <td style={{ color: s.direction === 'BUY' ? 'var(--success)' : 'var(--critical)', fontWeight: 700 }}>
                    {s.direction}
                  </td>
                  <td style={{ fontSize: '0.8rem' }}>{s.price > 0 ? s.price.toFixed(5) : '—'}</td>
                  <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{s.validity_window || '—'}</td>
                  <td style={{ textAlign: 'center', fontSize: '0.9rem' }}>
                    {s.signal_taken
                      ? <span style={{ color: 'var(--success)' }} title="Trade opened from this signal">✅</span>
                      : <span style={{ color: 'var(--text-secondary)', opacity: 0.4 }}>—</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Live Log Feed (improved terminal)
// ---------------------------------------------------------------------------

function LiveFeed({ logs }) {
  const ref = useRef(null)
  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight
  }, [logs])

  return (
    <div className="terminal" ref={ref}>
      {logs.length === 0 && (
        <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', padding: '0.5rem' }}>
          Waiting for events...
        </div>
      )}
      {logs.map((log, i) => (
        <div key={i} className="log-entry">
          <span className="log-time">[{toLocalTime(log.timestamp)?.toLocaleTimeString() ?? '—'}]</span>
          <span className={`log-type type-${log.event_type}`}>{log.event_type}</span>
          <span className="log-msg" style={{ color: log.status === 'CRITICAL' ? 'var(--critical)' : 'inherit' }}>
            {log.message}
            {log.meta_data && (
              <span style={{ color: 'var(--text-secondary)', marginLeft: 8, fontSize: '0.72rem' }}>
                {JSON.stringify(log.meta_data)}
              </span>
            )}
          </span>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Sidebar
// ---------------------------------------------------------------------------

function useTelegramStatus() {
  const [tg, setTg] = useState(null)
  useEffect(() => {
    const fetch_ = () =>
      fetch(`${API}/api/telegram/status`)
        .then(r => r.ok ? r.json() : null)
        .then(d => setTg(d))
        .catch(() => setTg(null))
    fetch_()
    const id = setInterval(fetch_, 15000)
    return () => clearInterval(id)
  }, [])
  return tg
}

function TelegramStatusCard() {
  const tg = useTelegramStatus()

  const statusColor = s => ({
    RUNNING: 'var(--success)',
    IDLE:    'var(--warning)',
    OFFLINE: 'var(--critical)',
    NOT_CONFIGURED: 'var(--text-secondary)',
  }[s] || 'var(--text-secondary)')

  function fmtAgo(secs) {
    if (secs === null || secs === undefined) return 'never'
    if (secs < 60) return `${secs}s ago`
    if (secs < 3600) return `${Math.floor(secs / 60)}m ago`
    if (secs < 86400) return `${Math.floor(secs / 3600)}h ago`
    return `${Math.floor(secs / 86400)}d ago`
  }

  return (
    <div className="card">
      <h4 className="card-title-sm">TELEGRAM BOT</h4>
      {!tg ? (
        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Loading...</div>
      ) : (
        <div className="conn-list">
          <div className="conn-row">
            <span>Status</span>
            <span style={{ color: statusColor(tg.status), fontWeight: 600 }}>
              {tg.status === 'RUNNING' && <span style={{ marginRight: 4 }}>●</span>}
              {tg.status}
            </span>
          </div>
          <div className="conn-row">
            <span>Last seen</span>
            <span style={{ color: tg.last_seen_seconds_ago !== null && tg.last_seen_seconds_ago < 300 ? 'var(--success)' : 'var(--text-secondary)' }}>
              {fmtAgo(tg.last_seen_seconds_ago)}
            </span>
          </div>
          <div className="conn-row">
            <span>Token</span>
            <span style={{ color: tg.token_set ? 'var(--success)' : 'var(--critical)' }}>
              {tg.token_set ? 'SET' : 'MISSING'}
            </span>
          </div>
          <div className="conn-row">
            <span>Chat ID</span>
            <span style={{ color: tg.chat_id_set ? 'var(--success)' : 'var(--critical)' }}>
              {tg.chat_id_set ? 'SET' : 'MISSING'}
            </span>
          </div>
          {tg.status === 'OFFLINE' && (
            <div style={{ marginTop: '0.5rem', fontSize: '0.72rem', color: 'var(--critical)', lineHeight: 1.4 }}>
              Bot not running. Start with:<br />
              <code style={{ fontSize: '0.7rem', opacity: 0.85 }}>python scripts/start_telegram_bot.py</code>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function useWhatsAppStatus() {
  const [wa, setWa] = useState(null)
  useEffect(() => {
    const fetch_ = () =>
      fetch(`${API}/api/whatsapp/status`)
        .then(r => r.ok ? r.json() : null)
        .then(d => setWa(d))
        .catch(() => setWa(null))
    fetch_()
    const id = setInterval(fetch_, 30000)
    return () => clearInterval(id)
  }, [])
  return wa
}

function WhatsAppStatusCard() {
  const wa = useWhatsAppStatus()
  const [qrUrl, setQrUrl] = useState(null)

  const statusColor = s => ({
    WORKING: 'var(--success)',
    STARTING: 'var(--warning)',
    SCAN_QR_CODE: 'var(--warning)',
    FAILED: 'var(--critical)',
    DISCONNECTED: 'var(--critical)',
    NO_SESSION: 'var(--text-secondary)'
  }[s] || 'var(--text-secondary)')

  async function handleRefreshQR() {
    try {
      const res = await fetch(`${API}/api/whatsapp/qr`, { method: 'POST' })
      const data = await res.json()
      if (data.qr_url) setQrUrl(data.qr_url)
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="card">
      <h4 className="card-title-sm">WHATSAPP NOTIFS</h4>
      {!wa ? (
        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Loading...</div>
      ) : (
        <div className="conn-list">
          <div className="conn-row">
            <span>Status</span>
            <span style={{ color: statusColor(wa.status), fontWeight: 600 }}>
              {wa.connected && <span style={{ marginRight: 4 }}>●</span>}
              {wa.status}
            </span>
          </div>
          <div className="conn-row">
            <span>Phone</span>
            <span style={{ color: wa.phone !== 'Not configured' ? 'var(--success)' : 'var(--critical)' }}>
              {wa.phone}
            </span>
          </div>
          {!wa.connected && (
            <div style={{ marginTop: '0.5rem', fontSize: '0.72rem' }}>
              <button className="bt-apply" onClick={handleRefreshQR} style={{width:'100%', marginBottom:4}}>Setup Session</button>
              {qrUrl && <div style={{marginTop:4, textAlign:'center'}}><a href={qrUrl} target="_blank" rel="noreferrer" style={{color:'var(--accent-primary)'}}>Open WAHA Dashboard</a></div>}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function useConnectivity() {
  const [health, setHealth] = React.useState(null)
  React.useEffect(() => {
    const check = () =>
      fetch(`${API}/api/health`)
        .then(r => r.json())
        .then(setHealth)
        .catch(() => setHealth(null))
    check()
    const id = setInterval(check, 15000)
    return () => clearInterval(id)
  }, [])
  return health
}

function ConnStatus({ status, okValues, activeValues }) {
  const isOk     = okValues?.includes(status)
  const isActive = activeValues?.includes(status)
  const color = isOk ? 'var(--success)' : isActive ? 'var(--accent-primary)' : status ? 'var(--critical)' : 'var(--text-secondary)'
  return <span style={{ color, fontWeight: 600 }}>{status || '…'}</span>
}

function Sidebar({ wsStatus }) {
  const health = useConnectivity()
  const mt5Status  = health?.mt5_bridge?.status  || '…'
  const pgStatus   = health?.postgresql?.status   || '…'
  const busStatus  = health?.event_bus?.status    || '…'

  return (
    <aside className="sidebar">
      <div className="card">
        <h4 className="card-title-sm">CONNECTIVITY</h4>
        <div className="conn-list">
          <div className="conn-row">
            <span>MT5 Bridge</span>
            <ConnStatus status={mt5Status} okValues={['ONLINE']} />
          </div>
          <div className="conn-row">
            <span>PostgreSQL</span>
            <ConnStatus status={pgStatus} okValues={['READY']} />
          </div>
          <div className="conn-row">
            <span>Event Bus</span>
            <ConnStatus status={busStatus} activeValues={['ACTIVE']} />
          </div>
          <div className="conn-row">
            <span>WebSocket</span>
            <span style={{ color: wsStatus === 'CONNECTED' ? 'var(--success)' : 'var(--critical)' }}>
              {wsStatus}
            </span>
          </div>
        </div>
      </div>

      <TelegramStatusCard />
      <WhatsAppStatusCard />

      <div className="card">
        <h4 className="card-title-sm">LOOKBACK</h4>
        <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
          Use the period selector above each chart to change the analytics window.
        </p>
      </div>

      <div className="card">
        <h4 className="card-title-sm">GO-LIVE CRITERIA</h4>
        <div className="criteria-list">
          <div className="criteria-row"><span className="criteria-label">Win Rate</span><span>≥ 90% of BT</span></div>
          <div className="criteria-row"><span className="criteria-label">Sharpe</span><span>≥ 0.8</span></div>
          <div className="criteria-row"><span className="criteria-label">Max DD</span><span>{'< 12%'}</span></div>
          <div className="criteria-row"><span className="criteria-label">Cons. losses</span><span>≤ 3</span></div>
        </div>
      </div>
    </aside>
  )
}


// ---------------------------------------------------------------------------
// AccountsTab
// ---------------------------------------------------------------------------

function AccountKpiStrip({ accountId, lookbackDays, refreshKey }) {
  const { data, loading } = useFetch(
    accountId ? `${API}/api/accounts/${accountId}/kpis?lookback_days=${lookbackDays}&_rk=${refreshKey}` : null,
    [accountId, lookbackDays, refreshKey]
  )
  if (!accountId) return <div className="kpi-strip"><div style={{color:'var(--text-secondary)',padding:'1rem'}}>Select an account above.</div></div>
  if (loading) return <div className="kpi-strip"><div style={{color:'var(--text-secondary)',padding:'1rem'}}>Loading KPIs...</div></div>
  if (!data || data.total_trades === 0) return <div className="kpi-strip"><div style={{color:'var(--text-secondary)',padding:'1rem'}}>No trades in this period.</div></div>
  const pnl = data.total_pnl || 0
  return (
    <div className="kpi-strip">
      <KpiCard label={`NET P&L (${lookbackDays}D)`} value={fmtZAR(pnl)}
        delta={`ROI ${data.roi_pct >= 0 ? '+' : ''}${data.roi_pct}%`}
        deltaPositive={pnl >= 0} accent={colorByVal(pnl)} />
      <KpiCard label="WIN RATE"
        value={`${data.win_rate}%`}
        delta={`${data.winning_trades}W / ${data.losing_trades}L`}
        deltaPositive={data.win_rate >= 50}
        accent={data.win_rate >= 90 ? 'var(--success)' : data.win_rate >= 70 ? 'var(--warning)' : 'var(--critical)'} />
      <KpiCard label="SHARPE RATIO"
        value={fmt(data.sharpe_ratio)}
        delta={data.sharpe_ratio >= 0.8 ? '> 0.8 target OK' : '< 0.8 target X'}
        deltaPositive={data.sharpe_ratio >= 0.8} />
      <KpiCard label="MAX DRAWDOWN"
        value={`${data.max_drawdown_pct}%`}
        delta={'< 12% limit ' + (data.max_drawdown_pct < 12 ? 'OK' : 'BREACH')}
        deltaPositive={data.max_drawdown_pct < 12} />
      <KpiCard label="PROFIT FACTOR"
        value={fmt(data.profit_factor)}
        delta={`RR ${data.avg_win && data.avg_loss ? fmt(Math.abs(data.avg_win / (data.avg_loss || 1))) : '—'}`}
        deltaPositive={data.profit_factor >= 1.2} />
      <KpiCard label="TOTAL TRADES"
        value={data.total_trades}
        delta={`${fmt(data.avg_win, 4)} avg W/L`}
        deltaPositive={data.avg_win > 0} />

      <div style={{ gridColumn: 'span 3', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '0.5rem' }}>
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: 12, border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: 8, letterSpacing: '0.05em' }}>MANUAL PERFORMANCE</div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
             <div style={{ fontSize: '1.25rem', fontWeight: 600, color: colorByVal(data.manual?.pnl) }}>{fmtZAR(data.manual?.pnl)}</div>
             <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{data.manual?.count} trades / {data.manual?.win_rate}% WR</div>
          </div>
        </div>
        <div style={{ background: 'rgba(0,229,255,0.02)', padding: '1rem', borderRadius: 12, border: '1px solid rgba(0,229,255,0.1)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: 8, letterSpacing: '0.05em' }}>BOT AUTOMATION</div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
             <div style={{ fontSize: '1.25rem', fontWeight: 600, color: colorByVal(data.bot?.pnl) }}>{fmtZAR(data.bot?.pnl)}</div>
             <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{data.bot?.count} trades / {data.bot?.win_rate}% WR</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function AccountEquityChart({ accountId, lookbackDays, refreshKey }) {
  const { data, loading, error } = useFetch(
    accountId ? `${API}/api/accounts/${accountId}/equity?lookback_days=${lookbackDays}&_rk=${refreshKey}` : null,
    [accountId, lookbackDays, refreshKey]
  )
  const chartData = React.useMemo(() => {
    if (!data?.equity_curve) return []
    return data.equity_curve.map(p => ({
      date: p.date ? String(p.date).slice(5) : '',
      equity: p.equity,
      pnl: p.pnl,
    }))
  }, [data])

  if (!accountId) return null
  if (loading) return <div className="chart-placeholder">Loading equity curve...</div>
  if (error || !chartData.length) return <div className="chart-placeholder">No equity data in this period</div>

  const minVal = Math.min(...chartData.map(d => d.equity))
  const domain = [Math.min(0, minVal * 1.05), 'auto']

  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={chartData} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="acctEquityGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#00e5ff" stopOpacity={0.25} />
            <stop offset="95%" stopColor="#00e5ff" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis dataKey="date" tick={{ fill: '#a0a0a0', fontSize: 10 }} axisLine={false} tickLine={false} interval="preserveStartEnd" />
        <YAxis tick={{ fill: '#a0a0a0', fontSize: 10 }} axisLine={false} tickLine={false} width={60}
          tickFormatter={v => `${(v / 1000).toFixed(1)}k`} domain={domain} />
        <Tooltip content={<CustomTooltip />} />
        <Area type="monotone" dataKey="equity" name="equity" stroke="#00e5ff" strokeWidth={2}
          fill="url(#acctEquityGrad)" dot={false} activeDot={{ r: 4, fill: '#00e5ff', strokeWidth: 0 }} />
      </AreaChart>
    </ResponsiveContainer>
  )
}

function AccountTradeTable({ accountId, lookbackDays, refreshKey }) {
  const [page, setPage] = React.useState(1)
  const [symbolFilter, setSymbolFilter] = React.useState('')
  const [appliedSymbol, setAppliedSymbol] = React.useState('')

  const url = accountId
    ? `${API}/api/accounts/${accountId}/trades?lookback_days=${lookbackDays}&page=${page}&page_size=50${appliedSymbol ? '&symbol=' + appliedSymbol : ''}&_rk=${refreshKey}`
    : null

  const { data, loading } = useFetch(url, [accountId, lookbackDays, page, appliedSymbol, refreshKey])

  React.useEffect(() => { setPage(1) }, [accountId, lookbackDays, appliedSymbol])

  if (!accountId) return null
  if (loading) return <div style={{ color: 'var(--text-secondary)', padding: '1rem' }}>Loading trades...</div>

  const trades = data?.trades || []
  const total = data?.total || 0
  const pages = data?.pages || 1

  return (
    <div>
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem', alignItems: 'center' }}>
        <input className="bt-filter" placeholder="Filter by symbol..." value={symbolFilter}
          onChange={e => setSymbolFilter(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && setAppliedSymbol(symbolFilter)}
          style={{ width: 180 }} />
        <button className="bt-apply" onClick={() => { setAppliedSymbol(symbolFilter); setPage(1) }}>Apply</button>
        {appliedSymbol && <button className="bt-clear" onClick={() => { setSymbolFilter(''); setAppliedSymbol(''); setPage(1) }}>Clear</button>}
        <span style={{ marginLeft: 'auto', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{total} trades</span>
      </div>
      {trades.length === 0 ? (
        <div style={{ color: 'var(--text-secondary)', padding: '1rem' }}>No trades found.</div>
      ) : (
        <>
          <table className="bt-table">
            <thead><tr>
              <th>Trade ID</th><th>Symbol</th><th>Entry</th><th>Exit</th>
              <th>P&L</th><th>Strategy</th><th>Date</th>
            </tr></thead>
            <tbody>
              {trades.map(t => (
                <tr key={t.trade_id}>
                  <td style={{ color: 'var(--accent-primary)', fontFamily: 'monospace' }}>#{t.trade_id}</td>
                  <td style={{ fontWeight: 600 }}>{t.pair}</td>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.78rem' }}>{t.entry_price}</td>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.78rem' }}>{t.exit_price}</td>
                  <td style={{ color: colorByVal(t.pnl), fontWeight: 600 }}>{t.pnl >= 0 ? '+' : ''}{t.pnl}</td>
                  <td>
                    {t.strategy_name === 'Manual' ? (
                      <span className="status-pill secondary" style={{ fontSize: '0.7rem' }}>MANUAL</span>
                    ) : (
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>{t.strategy_name}</span>
                        <span style={{ fontSize: '0.65rem', color: 'var(--accent-primary)', opacity: 0.7 }}>AUTOMATED</span>
                      </div>
                    )}
                  </td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>
                    {t.opened_at ? (
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span>{toLocalTime(t.opened_at)?.toLocaleDateString() ?? '—'}</span>
                        <span style={{ fontSize: '0.65rem', opacity: 0.6 }}>{toLocalTime(t.opened_at)?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) ?? '—'}</span>
                      </div>
                    ) : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {pages > 1 && (
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem', justifyContent: 'center' }}>
              <button className="bt-apply" onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Prev</button>
              <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', alignSelf: 'center' }}>
                {page} / {pages}
              </span>
              <button className="bt-apply" onClick={() => setPage(p => Math.min(pages, p + 1))} disabled={page === pages}>Next</button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

function AccountSymbolBreakdown({ accountId, lookbackDays, refreshKey }) {
  const { data, loading } = useFetch(
    accountId ? `${API}/api/accounts/${accountId}/by-symbol?lookback_days=${lookbackDays}&_rk=${refreshKey}` : null,
    [accountId, lookbackDays, refreshKey]
  )
  if (!accountId) return null
  if (loading) return <div style={{ color: 'var(--text-secondary)', padding: '1rem' }}>Loading...</div>
  const symbols = data?.by_symbol || []
  if (!symbols.length) return <div style={{ color: 'var(--text-secondary)', padding: '1rem' }}>No symbol data.</div>

  return (
    <table className="bt-table">
      <thead><tr>
        <th>Symbol</th><th>Trades</th><th>Net P&L</th><th>Win Rate</th>
      </tr></thead>
      <tbody>
        {symbols.map(s => (
          <tr key={s.symbol}>
            <td style={{ fontWeight: 600 }}>{s.symbol}</td>
            <td>{s.trades}</td>
            <td style={{ color: colorByVal(s.net_pnl), fontWeight: 600 }}>
              {s.net_pnl >= 0 ? '+' : ''}{s.net_pnl}
            </td>
            <td style={{ color: s.win_rate >= 90 ? 'var(--success)' : s.win_rate >= 60 ? 'var(--warning)' : 'var(--critical)' }}>
              {s.win_rate}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

function AccountsTab({ lookbackDays }) {
  const { data: accountList, loading: loadingAccounts } = useFetch(`${API}/api/accounts`, [])
  const [selectedId, setSelectedId] = React.useState(null)
  const [refreshKey, setRefreshKey] = React.useState(0)
  const [syncing, setSyncing] = React.useState(false)

  // Auto-select first account once loaded
  React.useEffect(() => {
    if (accountList?.length && selectedId === null) {
      setSelectedId(accountList[0].account_id)
    }
  }, [accountList, selectedId])

  const handleSync = async () => {
    setSyncing(true)
    try {
      const r = await fetch(`${API}/api/accounts/sync`, { method: 'POST' })
      const d = await r.json()
      if (d.status === 'success') {
        setRefreshKey(k => k + 1)
      } else {
        alert("Sync failed: " + d.message)
      }
    } catch (e) {
      alert("Sync error: " + e)
    } finally {
      setSyncing(false)
    }
  }

  const selectedAccount = accountList?.find(a => a.account_id === selectedId)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

      {/* Account switcher */}
      <div className="card" style={{ padding: '1rem 1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)' }}>Account Profile</span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Sync your MT5 history below</span>
          </div>
          {loadingAccounts ? (
            <span style={{ color: 'var(--text-secondary)' }}>Loading accounts...</span>
          ) : (
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {(accountList || []).map(a => (
                <button
                  key={a.account_id}
                  onClick={() => setSelectedId(a.account_id)}
                  style={{
                    padding: '0.4rem 1rem',
                    borderRadius: '6px',
                    border: selectedId === a.account_id ? '1px solid var(--accent-primary)' : '1px solid rgba(255,255,255,0.15)',
                    background: selectedId === a.account_id ? 'rgba(0,229,255,0.12)' : 'rgba(255,255,255,0.05)',
                    color: selectedId === a.account_id ? 'var(--accent-primary)' : 'var(--text-secondary)',
                    cursor: 'pointer',
                    fontWeight: selectedId === a.account_id ? 700 : 400,
                    fontSize: '0.85rem',
                    transition: 'all 0.15s',
                  }}
                >
                  {a.account_type}
                  <span style={{ fontSize: '0.7rem', marginLeft: '0.4rem', opacity: 0.7 }}>
                    ({a.trade_count} trades)
                  </span>
                </button>
              ))}
            </div>
          )}
          
          <button 
            className={`bt-apply ${syncing ? 'loading' : ''}`} 
            onClick={handleSync} 
            disabled={syncing}
            style={{ 
              marginLeft: 'auto', 
              background: 'var(--accent-primary)', 
              color: '#000', 
              fontWeight: 700,
              padding: '0.5rem 1.25rem'
            }}
          >
            {syncing ? 'Syncing...' : 'SYNC MT5 HISTORY'}
          </button>
        </div>
        {selectedAccount && (
          <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(255,255,255,0.05)', display: 'flex', gap: '1.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
             <span><strong>Broker:</strong> {selectedAccount.broker}</span>
             <span><strong>Currency:</strong> {selectedAccount.currency}</span>
             <span><strong>Initial Balance:</strong> {selectedAccount.initial_balance?.toLocaleString()}</span>
             {selectedAccount.notes && <span><strong>Notes:</strong> {selectedAccount.notes}</span>}
          </div>
        )}
      </div>

      {/* KPI strip */}
      <div className="card" style={{ padding: '0' }}>
        <AccountKpiStrip accountId={selectedId} lookbackDays={lookbackDays} />
      </div>

      {/* Equity curve */}
      <div className="card">
        <div className="card-head" style={{ marginBottom: '0.75rem' }}>
          <h3 className="card-h">Equity Curve</h3>
          <span className="live-dot"><span className="pulse" />LIVE</span>
        </div>
        <AccountEquityChart accountId={selectedId} lookbackDays={lookbackDays} />
      </div>

      {/* Trade history + symbol breakdown side by side */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.25rem' }}>
        <div className="card">
          <div className="card-head" style={{ marginBottom: '0.75rem' }}>
            <h3 className="card-h">Trade History</h3>
          </div>
          <AccountTradeTable accountId={selectedId} lookbackDays={lookbackDays} />
        </div>
        <div className="card">
          <div className="card-head" style={{ marginBottom: '0.75rem' }}>
            <h3 className="card-h">By Symbol</h3>
          </div>
          <AccountSymbolBreakdown accountId={selectedId} lookbackDays={lookbackDays} />
        </div>
      </div>

    </div>
  )
}

// ---------------------------------------------------------------------------
// SignalsTab  – live signal monitor with per-account filtering
// ---------------------------------------------------------------------------

function SignalsTab() {
  const [sigHours, setSigHours] = React.useState(24)
  const [accountFilter, setAccountFilter] = React.useState('all')

  const { data: accountList } = useFetch(`${API}/api/accounts`, [])
  const { data: sigData, loading, lastSync, refetch } = usePolling(
    `${API}/api/papertrades/signals?lookback_hours=${sigHours}&limit=200`,
    30000
  )

  const allSignals = sigData?.signals || []

  const signals = accountFilter === 'all'
    ? allSignals
    : accountFilter === 'unlinked'
      ? allSignals.filter(s => !s.account_id)
      : allSignals.filter(s => String(s.account_id) === accountFilter)

  const taken    = allSignals.filter(s => s.signal_taken).length
  const takenPct = allSignals.length ? Math.round(taken / allSignals.length * 100) : 0

  // Per-account counts for filter bar
  const accountCounts = {}
  for (const s of allSignals) {
    const key = s.account_id ? String(s.account_id) : 'unlinked'
    accountCounts[key] = (accountCounts[key] || 0) + 1
  }

  const pill = (active, color) => ({
    padding: '0.2rem 0.7rem', borderRadius: 12, border: '1px solid', cursor: 'pointer', fontSize: '0.75rem',
    borderColor: active ? (color || 'var(--accent-primary)') : 'rgba(255,255,255,0.15)',
    background:  active ? `${color ? color.replace(')', ',0.12)').replace('rgb', 'rgba') : 'rgba(0,229,255,0.12)'}` : 'transparent',
    color:       active ? (color || 'var(--accent-primary)') : 'var(--text-secondary)',
  })

  return (
    <>
      {/* Stats strip */}
      <div className="kpi-strip" style={{ marginBottom: '1rem' }}>
        <div className="kpi-card">
          <div className="kpi-label">Total Signals</div>
          <div className="kpi-value">{allSignals.length}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Taken → Trade</div>
          <div className="kpi-value" style={{ color: 'var(--success)' }}>{taken}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Take Rate</div>
          <div className="kpi-value">{takenPct}%</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Showing</div>
          <div className="kpi-value">{sigHours === 168 ? '7d' : `${sigHours}h`}</div>
        </div>
      </div>

      <div className="card">
        {/* Card header */}
        <div className="card-head" style={{ flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.75rem' }}>
          <h3 className="card-h">Signal Monitor</h3>
          <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center', flexWrap: 'wrap' }}>
            {[6, 24, 48, 168].map(h => (
              <button key={h} onClick={() => setSigHours(h)} style={{
                padding: '0.2rem 0.6rem', borderRadius: 4, border: '1px solid', cursor: 'pointer', fontSize: '0.75rem',
                borderColor: sigHours === h ? 'var(--accent-primary)' : 'rgba(255,255,255,0.15)',
                background:  sigHours === h ? 'rgba(0,229,255,0.12)' : 'transparent',
                color:       sigHours === h ? 'var(--accent-primary)' : 'var(--text-secondary)',
              }}>{h === 168 ? '7d' : `${h}h`}</button>
            ))}
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', marginLeft: 4 }}>
              {lastSync ? `↻ ${lastSync.toLocaleTimeString()}` : 'Loading…'}
            </span>
            <button onClick={refetch} style={{
              padding: '0.2rem 0.6rem', borderRadius: 4, border: '1px solid rgba(255,255,255,0.15)',
              background: 'transparent', color: 'var(--text-secondary)', cursor: 'pointer', fontSize: '0.75rem',
            }}>Refresh</button>
          </div>
        </div>

        {/* Account filter pills */}
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
          <button onClick={() => setAccountFilter('all')} style={pill(accountFilter === 'all')}>
            All ({allSignals.length})
          </button>
          {(accountList || []).map(a => {
            const cnt = accountCounts[String(a.account_id)] || 0
            if (cnt === 0) return null
            const isDemo = a.account_type === 'DEMO'
            const isLive = a.account_type === 'LIVE'
            const activeColor = isLive ? '#00e676' : isDemo ? '#00e5ff' : undefined
            return (
              <button key={a.account_id}
                onClick={() => setAccountFilter(String(a.account_id))}
                style={{
                  padding: '0.2rem 0.7rem', borderRadius: 12, border: '1px solid', cursor: 'pointer', fontSize: '0.75rem',
                  borderColor: accountFilter === String(a.account_id) ? (activeColor || 'var(--accent-primary)') : 'rgba(255,255,255,0.15)',
                  background:  accountFilter === String(a.account_id) ? `${isLive ? 'rgba(0,230,118,0.12)' : isDemo ? 'rgba(0,229,255,0.12)' : 'rgba(255,255,255,0.08)'}` : 'transparent',
                  color:       accountFilter === String(a.account_id) ? (activeColor || 'var(--accent-primary)') : 'var(--text-secondary)',
                }}
              >
                {a.account_name} · {a.account_type} ({cnt})
              </button>
            )
          })}
          {accountCounts['unlinked'] > 0 && (
            <button onClick={() => setAccountFilter('unlinked')} style={{
              padding: '0.2rem 0.7rem', borderRadius: 12, border: '1px solid', cursor: 'pointer', fontSize: '0.75rem',
              borderColor: accountFilter === 'unlinked' ? 'rgba(255,180,0,0.6)' : 'rgba(255,255,255,0.15)',
              background:  accountFilter === 'unlinked' ? 'rgba(255,180,0,0.1)' : 'transparent',
              color:       accountFilter === 'unlinked' ? '#ffb400' : 'var(--text-secondary)',
            }}>Pending / Untaken ({accountCounts['unlinked']})</button>
          )}
        </div>

        {/* Signals table */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8rem' }}>
            <thead>
              <tr style={{ color: 'var(--text-secondary)', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                {['Time', 'Account', 'Strategy', 'Pair', 'TF', 'Dir', 'Price', 'Valid', 'Profit', 'Status'].map((h, i) => (
                  <th key={h} style={{ textAlign: (i === 6 || i === 8) ? 'right' : i === 9 ? 'center' : 'left', padding: '0.4rem 0.5rem', fontWeight: 500 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr><td colSpan={10} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>Loading signals...</td></tr>
              )}
              {!loading && signals.length === 0 && (
                <tr><td colSpan={10} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>No signals in this window.</td></tr>
              )}
              {signals.map((s, i) => (
                <tr key={s.signal_id || i}
                  style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', transition: 'background 0.15s' }}
                  onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.03)' }}
                  onMouseLeave={e => { e.currentTarget.style.background = '' }}
                >
                  <td style={{ padding: '0.4rem 0.5rem', color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>
                    {toLocalTime(s.timestamp)?.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td style={{ padding: '0.4rem 0.5rem' }}>
                    {s.account_name && s.account_name !== '—'
                      ? <span style={{
                          padding: '0.15rem 0.45rem', borderRadius: 10, fontSize: '0.72rem', fontWeight: 600,
                          background: s.account_type === 'LIVE' ? 'rgba(0,230,118,0.12)' : s.account_type === 'DEMO' ? 'rgba(0,229,255,0.10)' : 'rgba(255,255,255,0.07)',
                          color: s.account_type === 'LIVE' ? '#00e676' : s.account_type === 'DEMO' ? '#00e5ff' : 'var(--text-secondary)',
                        }}>{s.account_name}</span>
                      : <span style={{ color: 'var(--text-secondary)', fontSize: '0.72rem' }}>-</span>
                    }
                  </td>
                  <td style={{ padding: '0.4rem 0.5rem', fontWeight: 500 }}>{s.strategy_name}</td>
                  <td style={{ padding: '0.4rem 0.5rem', fontWeight: 600, color: 'var(--accent-primary)' }}>{s.pair}</td>
                  <td style={{ padding: '0.4rem 0.5rem', color: 'var(--text-secondary)' }}>{s.timeframe}</td>
                  <td style={{ padding: '0.4rem 0.5rem' }}>
                    <span style={{
                      padding: '0.15rem 0.45rem', borderRadius: 4, fontWeight: 700, fontSize: '0.72rem',
                      background: s.direction === 'BUY' ? 'rgba(0,230,118,0.15)' : 'rgba(255,69,58,0.15)',
                      color: s.direction === 'BUY' ? 'var(--success)' : 'var(--critical)',
                    }}>{s.direction}</span>
                  </td>
                  <td style={{ padding: '0.4rem 0.5rem', textAlign: 'right', fontFamily: 'monospace' }}>
                    {s.price > 0 ? s.price.toFixed(5) : '-'}
                  </td>
                  <td style={{ padding: '0.4rem 0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>{s.validity_window || '-'}</td>
                  <td style={{ padding: '0.4rem 0.5rem', textAlign: 'right', fontFamily: 'monospace' }}>
                    {s.signal_taken ? (
                      <span style={{ color: s.trade_pnl >= 0 ? '#00e676' : '#ff453a', fontWeight: 600 }}>
                        {s.trade_pnl >= 0 ? '+' : ''}{s.trade_pnl.toFixed(2)}
                      </span>
                    ) : '-'}
                  </td>
                  <td style={{ padding: '0.4rem 0.5rem', textAlign: 'center' }}>
                    {s.signal_taken
                      ? <span title="Trade opened from this signal" style={{ 
                          color: s.trade_status === 'OPENED' ? '#ffb400' : 'var(--success)', 
                          fontSize: '0.82rem', fontWeight: 600 
                        }}>
                          {s.trade_status === 'OPENED' ? 'Running' : 'Closed'}
                        </span>
                      : <span title="No trade opened yet" style={{ color: 'var(--text-secondary)', fontSize: '0.82rem' }}>Pending</span>
                    }
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={{ marginTop: '0.75rem', fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
          Showing {signals.length} of {allSignals.length} signals &middot; Auto-refresh every 30s
        </div>
      </div>
    </>
  )
}

// ---------------------------------------------------------------------------
// Main App
// ---------------------------------------------------------------------------

const TABS = ['Overview', 'Performance', 'Strategies', 'Backtests', 'Accounts', 'Signals', 'Logs']

export default function App() {
  const [tab, setTab] = useState('Overview')
  const [lookbackDays, setLookbackDays] = useState(30)
  const [logs, setLogs] = useState([])
  const [wsStatus, setWsStatus] = useState('CONNECTING')
  const socketRef = useRef(null)

  // WebSocket for live log stream
  useEffect(() => {
    fetch(`${API}/api/logs`)
      .then(r => r.json())
      .then(d => setLogs(Array.isArray(d) ? d.reverse() : []))
      .catch(() => {})

    const connect = () => {
      const wsProto = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const ws = new WebSocket(`${wsProto}//${window.location.host}/api/ws/logs`)
      socketRef.current = ws
      ws.onopen = () => setWsStatus('CONNECTED')
      ws.onmessage = e => {
        try {
          const msg = JSON.parse(e.data)
          setLogs(prev => [...prev, msg].slice(-300))
        } catch {}
      }
      ws.onclose = () => {
        setWsStatus('DISCONNECTED')
        setTimeout(connect, 3000)
      }
      ws.onerror = () => setWsStatus('ERROR')
    }

    connect()
    return () => socketRef.current?.close()
  }, [])

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo-mark">T</div>
          <span className="logo-text">TRADEPANEL</span>
          <span className="logo-sub">HUB v2.1-PERF</span>
        </div>

        {/* Tabs */}
        <nav className="tab-nav">
          {TABS.map(t => (
            <button
              key={t}
              className={`tab-btn ${tab === t ? 'active' : ''}`}
              onClick={() => setTab(t)}
            >
              {t}
              {t === 'Backtests' && <span className="tab-badge">DB</span>}
              {t === 'Signals' && <span className="tab-badge" style={{background:'rgba(0,230,118,0.15)',color:'#00e676',borderColor:'rgba(0,230,118,0.3)'}}>LIVE</span>}
            </button>
          ))}
        </nav>

        <div className="header-right">
          <select
            className="period-select"
            value={lookbackDays}
            onChange={e => setLookbackDays(Number(e.target.value))}
          >
            <option value={7}>7 days</option>
            <option value={14}>14 days</option>
            <option value={30}>30 days</option>
            <option value={60}>60 days</option>
            <option value={90}>90 days</option>
          </select>
          <div className="status-badge">
            <div className={`pulse ${wsStatus !== 'CONNECTED' ? 'offline' : ''}`}
              style={{ backgroundColor: wsStatus === 'CONNECTED' ? 'var(--success)' : 'var(--critical)' }} />
            {wsStatus}
          </div>
        </div>
      </header>

      {/* Sidebar + Main */}
      <Sidebar wsStatus={wsStatus} />

      <main className="main-content">

        {/* -- OVERVIEW TAB -- */}
        {tab === 'Overview' && (
          <>
            <KpiStrip lookbackDays={lookbackDays} />
            
            <ConfigOverview />

            <div className="two-col" style={{ gridTemplateColumns: '3fr 2fr' }}>
               <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <WfoIntelligencePanel />
                  <StrategyIntelligenceTable />
               </div>
               <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <ActivityFeed />
                  <SignalsMonitor />
               </div>
            </div>

            <div className="two-col">
              <div className="card chart-card">
                <div className="card-head">
                  <h3 className="card-h">Equity Curve</h3>
                  <span className="live-dot">LIVE</span>
                </div>
                <EquityChart lookbackDays={lookbackDays} />
                <div style={{ marginTop: 16 }}>
                  <div className="card-sub">Daily P&L</div>
                  <DailyPnlChart lookbackDays={lookbackDays} />
                </div>
              </div>

              <div className="card">
                <div className="card-head">
                  <h3 className="card-h">System Log</h3>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{logs.length} events</span>
                </div>
                <LiveFeed logs={logs.slice(-50)} />
              </div>
            </div>
          </>
        )}

        {/* -- STRATEGIES TAB -- */}
        {tab === 'Strategies' && (
          <div className="card">
            <div className="card-head" style={{ marginBottom: '1rem' }}>
              <h3 className="card-h">Strategy Performance -- {lookbackDays}d window</h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Click column headers to sort &middot; Go-live criteria: WR &ge; 90%, Sharpe &ge; 0.8, DD &lt; 12%
              </span>
            </div>
            <StrategyTable lookbackDays={lookbackDays} />
          </div>
        )}

        {/* -- BACKTESTS TAB -- */}
        {tab === 'Backtests' && (
          <div className="card">
            <div className="card-head" style={{ marginBottom: '1rem' }}>
              <h3 className="card-h">Backtest Run History</h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Stored in DB &middot; click Restore to retrieve params + metrics snapshot
              </span>
            </div>
            <BacktestTable />
          </div>
        )}

        {/* -- ACCOUNTS TAB -- */}
        {tab === 'Accounts' && (
          <AccountsTab lookbackDays={lookbackDays} />
        )}

        {/* -- PERFORMANCE TAB -- */}
        {tab === 'Performance' && (
          <PerformanceDashboard lookbackDays={lookbackDays} />
        )}

        {/* -- SIGNALS TAB -- */}
        {tab === 'Signals' && (
          <SignalsTab />
        )}

        {/* -- LOGS TAB -- */}
        {tab === 'Logs' && (
          <div className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <div className="card-head" style={{ marginBottom: '1rem' }}>
              <h3 className="card-h">System Log Publication</h3>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{logs.length} events in buffer</span>
            </div>
            <LiveFeed logs={logs} />
          </div>
        )}

      </main>
    </div>
    )
}

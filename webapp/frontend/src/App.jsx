import React, { useState, useEffect, useRef, useCallback } from 'react'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, BarChart, Bar, Cell
} from 'recharts'
import './App.css'

const API = 'http://localhost:8000'

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function fmt(val, decimals = 2) {
  if (val === null || val === undefined) return '—'
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

function useFetch(url, deps = []) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(url)
      .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
      .then(d => { setData(d); setLoading(false) })
      .catch(e => { setError(String(e)); setLoading(false) })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  return { data, loading, error }
}

// ---------------------------------------------------------------------------
// KPI Card
// ---------------------------------------------------------------------------

function KpiCard({ label, value, delta, deltaPositive, unit, accent }) {
  return (
    <div className="kpi-card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value" style={{ color: accent || 'var(--text-primary)' }}>
        {value ?? <span style={{ color: 'var(--text-secondary)' }}>—</span>}
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
      delta: s ? `ROI ${fmtPct(s.roi_pct / 100)}` : undefined,
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
  const [sortKey, setSortKey] = useState('net_profit')
  const [sortDir, setSortDir] = useState('desc')

  const rows = React.useMemo(() => {
    if (!data?.strategies) return []
    return Object.entries(data.strategies).map(([name, m]) => ({ name, ...m }))
  }, [data])

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

  if (loading) return <div className="table-placeholder">Loading strategy metrics...</div>
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
                <td className="strat-name">{s.name.replace(/_/g, ' ')}</td>
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
  const [filter, setFilter] = useState({ strategy: '', status: '' })
  const [applied, setApplied] = useState({ strategy: '', status: '' })

  const url = React.useMemo(() => {
    const p = new URLSearchParams({ limit: '100' })
    if (applied.strategy) p.set('strategy', applied.strategy)
    if (applied.status) p.set('status', applied.status)
    return `${API}/api/backtests?${p}`
  }, [applied])

  const { data, loading, error } = useFetch(url, [url])
  const { data: stats } = useFetch(`${API}/api/backtests/stats/summary`, [])

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
      <div className="bt-filters">
        <input
          className="bt-input"
          placeholder="Filter strategy..."
          value={filter.strategy}
          onChange={e => setFilter(f => ({ ...f, strategy: e.target.value }))}
          onKeyDown={e => e.key === 'Enter' && setApplied(filter)}
        />
        <select className="bt-select" value={filter.status} onChange={e => { setFilter(f => ({ ...f, status: e.target.value })); setApplied(f => ({ ...f, status: e.target.value })) }}>
          <option value="">All statuses</option>
          <option value="PASS">PASS</option>
          <option value="REVIEW">REVIEW</option>
          <option value="FAIL">FAIL</option>
        </select>
        <button className="bt-btn" onClick={() => setApplied(filter)}>Apply</button>
        <button className="bt-btn secondary" onClick={() => { setFilter({ strategy: '', status: '' }); setApplied({ strategy: '', status: '' }) }}>Clear</button>
        <span style={{ marginLeft: 'auto', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          {data?.total ?? 0} runs
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
                    {r.run_date ? new Date(r.run_date).toLocaleDateString() : '—'}
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
            Restored at {new Date(restoreData.restored_at).toLocaleString()}
          </div>
        </div>
      )}
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
          <span className="log-time">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
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

function Sidebar({ wsStatus }) {
  return (
    <aside className="sidebar">
      <div className="card">
        <h4 className="card-title-sm">CONNECTIVITY</h4>
        <div className="conn-list">
          <div className="conn-row">
            <span>MT5 Bridge</span>
            <span style={{ color: 'var(--success)' }}>ONLINE</span>
          </div>
          <div className="conn-row">
            <span>PostgreSQL</span>
            <span style={{ color: 'var(--success)' }}>READY</span>
          </div>
          <div className="conn-row">
            <span>Event Bus</span>
            <span style={{ color: 'var(--accent-primary)' }}>ACTIVE</span>
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

function AccountKpiStrip({ accountId, lookbackDays }) {
  const { data, loading } = useFetch(
    accountId ? `${API}/api/accounts/${accountId}/kpis?lookback_days=${lookbackDays}` : null,
    [accountId, lookbackDays]
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
    </div>
  )
}

function AccountEquityChart({ accountId, lookbackDays }) {
  const { data, loading, error } = useFetch(
    accountId ? `${API}/api/accounts/${accountId}/equity?lookback_days=${lookbackDays}` : null,
    [accountId, lookbackDays]
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

function AccountTradeTable({ accountId, lookbackDays }) {
  const [page, setPage] = React.useState(1)
  const [symbolFilter, setSymbolFilter] = React.useState('')
  const [appliedSymbol, setAppliedSymbol] = React.useState('')

  const url = accountId
    ? `${API}/api/accounts/${accountId}/trades?lookback_days=${lookbackDays}&page=${page}&page_size=50${appliedSymbol ? '&symbol=' + appliedSymbol : ''}`
    : null

  const { data, loading } = useFetch(url, [accountId, lookbackDays, page, appliedSymbol])

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
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>{t.strategy_name}</td>
                  <td style={{ color: 'var(--text-secondary)', fontSize: '0.78rem' }}>
                    {t.opened_at ? new Date(t.opened_at).toLocaleDateString() : '—'}
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

function AccountSymbolBreakdown({ accountId, lookbackDays }) {
  const { data, loading } = useFetch(
    accountId ? `${API}/api/accounts/${accountId}/by-symbol?lookback_days=${lookbackDays}` : null,
    [accountId, lookbackDays]
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

  // Auto-select first account once loaded
  React.useEffect(() => {
    if (accountList?.length && selectedId === null) {
      setSelectedId(accountList[0].account_id)
    }
  }, [accountList, selectedId])

  const selectedAccount = accountList?.find(a => a.account_id === selectedId)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

      {/* Account switcher */}
      <div className="card" style={{ padding: '1rem 1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <span style={{ fontWeight: 700, fontSize: '1rem' }}>Account Profile</span>
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
          {selectedAccount && (
            <span style={{ marginLeft: 'auto', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
              {selectedAccount.broker} &middot; {selectedAccount.currency} &middot; Balance: {selectedAccount.initial_balance?.toLocaleString()}
            </span>
          )}
        </div>
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
// Main App
// ---------------------------------------------------------------------------

const TABS = ['Overview', 'Strategies', 'Backtests', 'Accounts', 'Logs']

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
      const ws = new WebSocket(`ws://localhost:8000/api/ws/logs`)
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
          <span className="logo-sub">HUB v2.0</span>
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
              {t === 'Accounts' && <span className="tab-badge" style={{background:'rgba(0,229,255,0.15)',color:'#00e5ff',borderColor:'rgba(0,229,255,0.3)'}}>NEW</span>}
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

        {/* ── OVERVIEW TAB ── */}
        {tab === 'Overview' && (
          <>
            <KpiStrip lookbackDays={lookbackDays} />

            <div className="two-col">
              <div className="card chart-card">
                <div className="card-head">
                  <h3 className="card-h">Equity Curve</h3>
                  <span className="live-dot">● LIVE</span>
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

        {/* ── STRATEGIES TAB ── */}
        {tab === 'Strategies' && (
          <div className="card">
            <div className="card-head" style={{ marginBottom: '1rem' }}>
              <h3 className="card-h">Strategy Performance — {lookbackDays}d window</h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Click column headers to sort · Go-live criteria: WR ≥ 90%, Sharpe ≥ 0.8, DD {'<'} 12%
              </span>
            </div>
            <StrategyTable lookbackDays={lookbackDays} />
          </div>
        )}

        {/* ── BACKTESTS TAB ── */}
        {tab === 'Backtests' && (
          <div className="card">
            <div className="card-head" style={{ marginBottom: '1rem' }}>
              <h3 className="card-h">Backtest Run History</h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Stored in DB · click Restore to retrieve params + metrics snapshot
              </span>
            </div>
            <BacktestTable />
          </div>
        )}

        {/* ── ACCOUNTS TAB ── */}
        {tab === 'Accounts' && (
          <AccountsTab lookbackDays={lookbackDays} />
        )}

        {/* ── LOGS TAB ── */}
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

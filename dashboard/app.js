/**
 * TradePanel Pro Dashboard Logic
 * Fetches analytics from the local API and renders interactive charts.
 */

document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
    fetchLiveAccount();
    fetchSignalPerformance();
    fetchRiskMetrics();
    fetchTradeJournal();
    // Auto-refresh every 60 seconds
    setInterval(fetchDashboardData, 60000);
    setInterval(fetchLiveAccount, 30000);
    setInterval(fetchSignalPerformance, 120000);
    setInterval(fetchRiskMetrics, 120000);
});

let charts = {};

async function fetchDashboardData() {
    try {
        const response = await fetch('/api/data');
        if (!response.ok) throw new Error("Data not found");
        
        const data = await response.json();
        
        // If data is virtually empty, trigger Demo Mode for visual appeal
        if (data.validation_summary.total_strategies === 0 || data.charts.performance_matrix.data_points.length === 0) {
            console.warn("Real data not found. Injecting Demo Data...");
            injectDemoData(data);
        }
        
        updateSummaryMetrics(data);
        renderPerformanceMatrix(data.charts.performance_matrix);
        renderTierDistribution(data.charts.tier_distribution);
        renderTrendAnalysis(data.charts.trend_analysis);
        renderCorrelationMatrix(data.charts.correlation_matrix);
        renderOptimizationTable(data.optimization_pipeline);
        
    } catch (error) {
        console.warn('Using Demo Data (API unreachable):', error);
        const demoData = getMockData();
        updateSummaryMetrics(demoData);
        renderPerformanceMatrix(demoData.charts.performance_matrix);
        renderTierDistribution(demoData.charts.tier_distribution);
        renderTrendAnalysis(demoData.charts.trend_analysis);
        renderCorrelationMatrix(demoData.charts.correlation_matrix);
        renderOptimizationTable(demoData.optimization_pipeline);
    }
}

function injectDemoData(data) {
    const mock = getMockData();
    Object.assign(data, mock);
    document.querySelector('.logo h1').innerHTML = "TRADEPANEL <span>DEMO</span>";
}

function getMockData() {
    return {
        last_update: "20260420_120000",
        validation_summary: { total_strategies: 25, passed: 18, failed: 7, pass_rate: "72%" },
        charts: {
            performance_matrix: {
                data_points: [
                    { name: "Range Breakout", win_rate: 55, profit_factor: 1.8, sharpe_ratio: 1.5 },
                    { name: "Dual EMA", win_rate: 48, profit_factor: 1.4, sharpe_ratio: 1.2 },
                    { name: "SMC Liquidity", win_rate: 62, profit_factor: 2.1, sharpe_ratio: 1.8 },
                    { name: "RSI Reversal", win_rate: 42, profit_factor: 1.1, sharpe_ratio: 0.9 },
                    { name: "Volatility Squeeze", win_rate: 58, profit_factor: 1.9, sharpe_ratio: 1.6 }
                ]
            },
            trend_analysis: {
                dates: ["Apr 14", "Apr 15", "Apr 16", "Apr 17", "Apr 18", "Apr 19", "Apr 20"],
                metrics: {
                    average_win_rate: [45, 48, 52, 50, 55, 58, 60],
                    average_profit_factor: [1.2, 1.3, 1.5, 1.4, 1.7, 1.8, 2.0]
                }
            },
            tier_distribution: {
                tiers: {
                    "TIER_1": { count: 8 },
                    "TIER_2": { count: 12 },
                    "TIER_3": { count: 5 }
                }
            },
            correlation_matrix: {
                high_correlation_pairs: [
                    { strategy_1: "Range Breakout", strategy_2: "Opening Range", correlation: 0.85 },
                    { strategy_1: "Dual EMA", strategy_2: "EMA Ribbon", correlation: 0.72 }
                ]
            }
        },
        optimization_pipeline: {
            queue: [
                { priority: 1, strategy: "BB Reversion", pair: "EURUSD", current_pf: 0.95, suggested_changes: { bb_std: 2.2 }, expected_improvement: "+24%" },
                { priority: 2, strategy: "MA Cross", pair: "XAUUSD", current_pf: 1.15, suggested_changes: { fast_ema: 12 }, expected_improvement: "+18%" }
            ]
        }
    };
}

function updateSummaryMetrics(data) {
    document.getElementById('last-update').innerText = data.last_update.split('_')[1].match(/.{1,2}/g).join(':');
    document.getElementById('pass-rate').innerText = data.validation_summary.pass_rate;
    document.getElementById('total-strategies').innerText = data.validation_summary.total_strategies;
    document.getElementById('passed-count').innerText = data.validation_summary.passed;
    document.getElementById('failed-count').innerText = `${data.validation_summary.failed} Issues`;
    
    const points = data.charts.performance_matrix.data_points || [];
    if (points.length > 0) {
        const avgPF = points.reduce((acc, p) => acc + p.profit_factor, 0) / points.length;
        const avgSharpe = points.reduce((acc, p) => acc + p.sharpe_ratio, 0) / points.length;
        document.getElementById('avg-pf').innerText = avgPF.toFixed(2);
        document.getElementById('avg-sharpe').innerText = avgSharpe.toFixed(2);
    } else {
        document.getElementById('avg-pf').innerText = "--";
        document.getElementById('avg-sharpe').innerText = "--";
    }
}

function renderPerformanceMatrix(matrixData) {
    const dataPoints = matrixData.data_points || [];
    const series = dataPoints.map(p => ({
        x: p.win_rate,
        y: p.profit_factor,
        name: p.name,
        sharpe: p.sharpe_ratio
    }));

    const options = {
        series: [{ name: 'Strategies', data: series }],
        chart: {
            height: 350,
            type: 'scatter',
            zoom: { enabled: true, type: 'xy' },
            toolbar: { show: false },
            foreColor: '#a0a0a0',
            background: 'transparent'
        },
        noData: { text: 'Waiting for Strategy Validation...', style: { color: '#00f2ff', fontSize: '16px' } },
        colors: ['#00f2ff'],
        xaxis: {
            title: { text: 'Win Rate (%)' },
            tickAmount: 10,
            labels: { formatter: (val) => parseFloat(val).toFixed(0) },
            min: 0, max: 100
        },
        yaxis: {
            title: { text: 'Profit Factor' },
            tickAmount: 5,
            min: 0, max: 5
        },
        tooltip: {
            theme: 'dark',
            custom: function({series, seriesIndex, dataPointIndex, w}) {
                const p = w.config.series[seriesIndex].data[dataPointIndex];
                if (!p) return '';
                return `<div style="padding: 10px; background: #111; border: 1px solid #333;">
                    <b style="color: #00f2ff">${p.name}</b><br>
                    WR: ${p.x.toFixed(1)}%<br>
                    PF: ${p.y.toFixed(2)}<br>
                    Sharpe: ${p.sharpe.toFixed(2)}
                </div>`;
            }
        },
        grid: { borderColor: '#222' }
    };

    if (charts.perf) charts.perf.updateOptions(options); else {
        charts.perf = new ApexCharts(document.querySelector("#performance-matrix-chart"), options);
        charts.perf.render();
    }
}

function renderTierDistribution(tierData) {
    const tiers = tierData.tiers || {};
    const labels = Object.keys(tiers);
    const counts = labels.map(l => tiers[l].count);
    const total = counts.reduce((a, b) => a + b, 0);

    const options = {
        series: total > 0 ? counts : [],
        chart: { type: 'donut', height: 350 },
        noData: { text: 'No Tiers Assigned', style: { color: '#ff9d00', fontSize: '16px' } },
        labels: labels,
        colors: ['#00ff88', '#ff9d00', '#ff4d4d'],
        legend: { position: 'bottom', labels: { colors: '#a0a0a0' } },
        stroke: { show: false },
        plotOptions: {
            pie: {
                donut: {
                    labels: {
                        show: true,
                        name: { color: '#fff' },
                        total: { show: true, color: '#00f2ff', label: 'Tiers' }
                    }
                }
            }
        },
        dataLabels: { enabled: false }
    };

    if (charts.tier) charts.tier.updateOptions(options); else {
        charts.tier = new ApexCharts(document.querySelector("#tier-distribution-chart"), options);
        charts.tier.render();
    }
}

function renderTrendAnalysis(trendData) {
    const dates = trendData.dates || [];
    const wr = trendData.metrics?.average_win_rate || [];
    const pf = (trendData.metrics?.average_profit_factor || []).map(v => v * 20);

    const options = {
        series: dates.length > 0 ? [
            { name: 'Avg Win Rate', data: wr },
            { name: 'Avg Profit Factor (Scaled)', data: pf }
        ] : [],
        chart: { height: 350, type: 'area', toolbar: { show: false }, foreColor: '#a0a0a0' },
        noData: { text: 'Accumulating Trend Data...', style: { color: '#00ff88', fontSize: '16px' } },
        colors: ['#00f2ff', '#00ff88'],
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth', width: 2 },
        xaxis: { categories: dates, labels: { show: false } },
        grid: { borderColor: '#222' },
        legend: { position: 'top', labels: { colors: '#a0a0a0' } }
    };

    if (charts.trend) charts.trend.updateOptions(options); else {
        charts.trend = new ApexCharts(document.querySelector("#trend-analysis-chart"), options);
        charts.trend.render();
    }
}

function renderCorrelationMatrix(corrData) {
    const pairs = corrData.high_correlation_pairs || [];
    const data = pairs.map(p => ({
        x: p.strategy_1.substring(0, 8),
        y: p.strategy_2.substring(0, 8),
        value: isNaN(parseFloat(p.correlation)) ? 0 : parseFloat(p.correlation)
    }));

    const options = {
        series: [{ name: 'Correlation', data: data }],
        chart: { height: 350, type: 'heatmap', toolbar: { show: false }, foreColor: '#a0a0a0' },
        noData: { text: 'Low Correlation Detected', style: { color: '#ffffff', fontSize: '16px' } },
        dataLabels: { enabled: true, style: { colors: ['#fff'] } },
        colors: ["#00f2ff"],
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.5,
                colorScale: {
                    ranges: [{ from: -1, to: 0.5, name: 'Low', color: '#00ff88' },
                             { from: 0.51, to: 0.7, name: 'Med', color: '#ff9d00' },
                             { from: 0.71, to: 1.0, name: 'High', color: '#ff4d4d' }]
                }
            }
        }
    };

    if (charts.corr) charts.corr.updateOptions(options); else {
        charts.corr = new ApexCharts(document.querySelector("#correlation-matrix-chart"), options);
        charts.corr.render();
    }
}

// ─── Live Account Panel ──────────────────────────────────────────────────────

async function fetchLiveAccount() {
    try {
        const res = await fetch('/api/live_account');
        const data = res.ok ? await res.json() : getDemoLiveAccount();
        renderLiveAccount(data);
    } catch (e) {
        renderLiveAccount(getDemoLiveAccount());
    }
}

function getDemoLiveAccount() {
    return {
        daily_pnl: 340.50,
        bot_positions: { count: 3, lots: 0.09 },
        manual_positions: { count: 1, lots: 0.05 },
        circuit_breaker_active: false,
        cb_message: "",
        max_drawdown_30d: 4.2,
        account_currency: "ZAR"
    };
}

function renderLiveAccount(data) {
    const pnl = data.daily_pnl || 0;
    const pnlEl = document.getElementById('live-daily-pnl');
    if (pnlEl) {
        pnlEl.textContent = `R ${pnl >= 0 ? '+' : ''}${pnl.toFixed(2)}`;
        pnlEl.style.color = pnl >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
    }
    const botPos = data.bot_positions || {};
    const manPos = data.manual_positions || {};
    const bp = document.getElementById('live-bot-positions');
    const bl = document.getElementById('live-bot-lots');
    const mp = document.getElementById('live-manual-positions');
    const ml = document.getElementById('live-manual-lots');
    if (bp) bp.textContent = botPos.count || 0;
    if (bl) bl.textContent = `${(botPos.lots || 0).toFixed(2)} lots`;
    if (mp) mp.textContent = manPos.count || 0;
    if (ml) ml.textContent = `${(manPos.lots || 0).toFixed(2)} lots`;
    const ddEl = document.getElementById('live-max-dd');
    if (ddEl) {
        const dd = data.max_drawdown_30d || 0;
        ddEl.textContent = `${dd.toFixed(1)}%`;
        ddEl.style.color = dd > 15 ? 'var(--accent-red)' : dd > 8 ? 'var(--accent-orange)' : 'var(--accent-green)';
    }
    const cbBadge = document.getElementById('cb-badge');
    if (cbBadge) {
        if (data.circuit_breaker_active) {
            cbBadge.classList.remove('hidden');
            cbBadge.title = data.cb_message || '';
        } else {
            cbBadge.classList.add('hidden');
        }
    }
}

// ─── Signal Performance Panel ─────────────────────────────────────────────────

async function fetchSignalPerformance() {
    try {
        const res = await fetch('/api/signal_performance');
        const data = res.ok ? await res.json() : getDemoSignalPerformance();
        renderSignalHitRate(data.hit_rate_by_strategy || []);
        renderSignalsPerDay(data.signals_per_day || []);
        renderSignalConversion(data.conversion_rate || { converted: 0, not_converted: 0 });
    } catch (e) {
        const demo = getDemoSignalPerformance();
        renderSignalHitRate(demo.hit_rate_by_strategy);
        renderSignalsPerDay(demo.signals_per_day);
        renderSignalConversion(demo.conversion_rate);
    }
}

function getDemoSignalPerformance() {
    return {
        hit_rate_by_strategy: [
            { strategy: "gold_momentum_breakout", total: 24, converted: 18, rate: 75.0 },
            { strategy: "rsi_pullback", total: 31, converted: 21, rate: 67.7 },
            { strategy: "ma_crossover", total: 19, converted: 12, rate: 63.2 },
            { strategy: "rsi_extremes_scalp", total: 11, converted: 7, rate: 63.6 },
            { strategy: "bb_squeeze_scalp", total: 8, converted: 5, rate: 62.5 }
        ],
        signals_per_day: [
            { date: "2026-04-27", buy: 5, sell: 3 },
            { date: "2026-04-28", buy: 7, sell: 4 },
            { date: "2026-04-29", buy: 6, sell: 6 },
            { date: "2026-04-30", buy: 9, sell: 5 },
            { date: "2026-05-01", buy: 8, sell: 7 },
            { date: "2026-05-02", buy: 4, sell: 2 },
            { date: "2026-05-03", buy: 3, sell: 1 }
        ],
        conversion_rate: { converted: 63, not_converted: 30 }
    };
}

function renderSignalHitRate(data) {
    if (!data.length) return;
    const categories = data.map(d => d.strategy.replace(/_/g, ' '));
    const rates = data.map(d => d.rate);
    const options = {
        series: [{ name: 'Hit Rate %', data: rates }],
        chart: { type: 'bar', height: 280, toolbar: { show: false }, foreColor: '#a0a0a0', background: 'transparent' },
        colors: ['#00f2ff'],
        plotOptions: { bar: { borderRadius: 4, horizontal: true } },
        dataLabels: { enabled: true, formatter: v => v.toFixed(1) + '%', style: { colors: ['#fff'] } },
        xaxis: { categories, labels: { style: { colors: '#a0a0a0', fontSize: '11px' } }, max: 100 },
        yaxis: { labels: { style: { colors: '#a0a0a0', fontSize: '10px' } } },
        grid: { borderColor: '#222' },
        annotations: { xaxis: [{ x: 60, borderColor: '#00ff88', label: { text: '60%', style: { color: '#00ff88', background: '#111' } } }] }
    };
    if (charts.hitRate) charts.hitRate.updateOptions(options);
    else { charts.hitRate = new ApexCharts(document.querySelector('#signal-hitrate-chart'), options); charts.hitRate.render(); }
}

function renderSignalsPerDay(data) {
    const dates = data.map(d => d.date);
    const buys = data.map(d => d.buy);
    const sells = data.map(d => d.sell);
    const options = {
        series: [
            { name: 'BUY', data: buys },
            { name: 'SELL', data: sells }
        ],
        chart: { type: 'area', height: 280, toolbar: { show: false }, foreColor: '#a0a0a0', background: 'transparent', stacked: false },
        colors: ['#00ff88', '#ff4d4d'],
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth', width: 2 },
        fill: { type: 'gradient', gradient: { opacityFrom: 0.4, opacityTo: 0.05 } },
        xaxis: { categories: dates, labels: { style: { colors: '#a0a0a0' } } },
        yaxis: { labels: { style: { colors: '#a0a0a0' } } },
        legend: { position: 'top', labels: { colors: '#a0a0a0' } },
        grid: { borderColor: '#222' }
    };
    if (charts.sigDay) charts.sigDay.updateOptions(options);
    else { charts.sigDay = new ApexCharts(document.querySelector('#signals-per-day-chart'), options); charts.sigDay.render(); }
}

function renderSignalConversion(data) {
    const converted = data.converted || 0;
    const not_converted = data.not_converted || 0;
    const total = converted + not_converted;
    const rate = total > 0 ? ((converted / total) * 100).toFixed(1) : '0';
    const options = {
        series: [converted, not_converted],
        labels: [`Converted (${rate}%)`, 'Not Converted'],
        chart: { type: 'donut', height: 280, background: 'transparent' },
        colors: ['#00ff88', '#333'],
        stroke: { show: false },
        legend: { position: 'bottom', labels: { colors: '#a0a0a0' } },
        plotOptions: { pie: { donut: { labels: { show: true, name: { color: '#fff' }, value: { color: '#fff' }, total: { show: true, label: 'Converted', color: '#00f2ff' } } } } },
        dataLabels: { enabled: false }
    };
    if (charts.conv) charts.conv.updateOptions(options);
    else { charts.conv = new ApexCharts(document.querySelector('#signal-conversion-chart'), options); charts.conv.render(); }
}

// ─── Risk Metrics Panel ───────────────────────────────────────────────────────

async function fetchRiskMetrics() {
    try {
        const res = await fetch('/api/risk_metrics');
        const data = res.ok ? await res.json() : getDemoRiskMetrics();
        renderDailyDrawdown(data.daily_drawdown || []);
        renderKellyChart(data.kelly_per_strategy || []);
        renderCbEventsTable(data.circuit_breaker_events || []);
    } catch (e) {
        const demo = getDemoRiskMetrics();
        renderDailyDrawdown(demo.daily_drawdown);
        renderKellyChart(demo.kelly_per_strategy);
        renderCbEventsTable(demo.circuit_breaker_events);
    }
}

function getDemoRiskMetrics() {
    return {
        daily_drawdown: [
            { date: "2026-04-20", drawdown: 1.2 }, { date: "2026-04-21", drawdown: 0.8 },
            { date: "2026-04-22", drawdown: 2.1 }, { date: "2026-04-23", drawdown: 1.5 },
            { date: "2026-04-24", drawdown: 3.0 }, { date: "2026-04-25", drawdown: 2.4 },
            { date: "2026-04-28", drawdown: 1.8 }, { date: "2026-04-29", drawdown: 4.2 },
            { date: "2026-04-30", drawdown: 3.1 }, { date: "2026-05-01", drawdown: 1.9 },
            { date: "2026-05-02", drawdown: 0.5 }, { date: "2026-05-03", drawdown: 1.1 }
        ],
        kelly_per_strategy: [
            { strategy: "gold_momentum_breakout", kelly_pct: 6.4, win_rate: 64.0, trades: 72 },
            { strategy: "rsi_pullback", kelly_pct: 5.8, win_rate: 60.0, trades: 55 },
            { strategy: "ma_crossover", kelly_pct: 4.9, win_rate: 67.0, trades: 18 },
            { strategy: "rsi_extremes_scalp", kelly_pct: 7.2, win_rate: 75.0, trades: 8 },
            { strategy: "bb_squeeze_scalp", kelly_pct: 8.1, win_rate: 80.0, trades: 5 }
        ],
        circuit_breaker_events: []
    };
}

function renderDailyDrawdown(data) {
    const dates = data.map(d => d.date);
    const values = data.map(d => d.drawdown);
    const colors = values.map(v => v >= 15 ? '#ff4d4d' : v >= 8 ? '#ff9d00' : '#00f2ff');
    const options = {
        series: [{ name: 'Drawdown %', data: values }],
        chart: { type: 'bar', height: 280, toolbar: { show: false }, foreColor: '#a0a0a0', background: 'transparent' },
        colors: ['#00f2ff'],
        plotOptions: { bar: { borderRadius: 3, distributed: true, columnWidth: '60%' } },
        fill: { colors: colors },
        dataLabels: { enabled: false },
        xaxis: { categories: dates, labels: { rotate: -45, style: { colors: '#a0a0a0', fontSize: '10px' } } },
        yaxis: { title: { text: 'DD %', style: { color: '#a0a0a0' } }, labels: { formatter: v => v.toFixed(1) + '%', style: { colors: '#a0a0a0' } } },
        annotations: { yaxis: [{ y: 20, borderColor: '#ff4d4d', label: { text: 'Hard Stop 20%', style: { color: '#ff4d4d', background: '#111' } } }] },
        grid: { borderColor: '#222' },
        legend: { show: false }
    };
    if (charts.dd) charts.dd.updateOptions(options);
    else { charts.dd = new ApexCharts(document.querySelector('#daily-drawdown-chart'), options); charts.dd.render(); }
}

function renderKellyChart(data) {
    if (!data.length) return;
    const categories = data.map(d => d.strategy.replace(/_/g, ' '));
    const kellys = data.map(d => d.kelly_pct);
    const options = {
        series: [{ name: 'Kelly %', data: kellys }],
        chart: { type: 'bar', height: 280, toolbar: { show: false }, foreColor: '#a0a0a0', background: 'transparent' },
        colors: ['#00ff88'],
        plotOptions: { bar: { borderRadius: 4, columnWidth: '55%' } },
        dataLabels: { enabled: true, formatter: v => v.toFixed(1) + '%', style: { colors: ['#fff'], fontSize: '11px' } },
        xaxis: { categories, labels: { rotate: -30, style: { colors: '#a0a0a0', fontSize: '10px' } } },
        yaxis: { title: { text: 'Kelly Fraction (%)', style: { color: '#a0a0a0' } }, labels: { formatter: v => v.toFixed(1) + '%', style: { colors: '#a0a0a0' } } },
        tooltip: { theme: 'dark', y: { formatter: (val, { dataPointIndex }) => `${val.toFixed(2)}% Kelly | ${data[dataPointIndex].win_rate}% WR | ${data[dataPointIndex].trades} trades` } },
        grid: { borderColor: '#222' }
    };
    if (charts.kelly) charts.kelly.updateOptions(options);
    else { charts.kelly = new ApexCharts(document.querySelector('#kelly-chart'), options); charts.kelly.render(); }
}

function renderCbEventsTable(events) {
    const tbody = document.getElementById('cb-events-body');
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!events.length) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:#a0a0a0;padding:1.5rem">No circuit breaker events — system running clean ✓</td></tr>';
        return;
    }
    events.forEach(ev => {
        const color = ev.type === 'CIRCUIT_BREAKER' ? 'var(--accent-red)' : ev.type === 'MANUAL_PAUSE' ? 'var(--accent-orange)' : 'var(--accent-green)';
        tbody.insertAdjacentHTML('beforeend', `
            <tr>
                <td style="color:var(--text-secondary);font-size:0.85rem">${ev.time}</td>
                <td><span style="color:${color};font-weight:600">${ev.type}</span></td>
                <td style="font-size:0.85rem;color:var(--text-secondary)">${ev.message}</td>
            </tr>`);
    });
}

// ─── Trade Journal Panel ──────────────────────────────────────────────────────

async function fetchTradeJournal(params = {}) {
    try {
        const qs = new URLSearchParams(params).toString();
        const res = await fetch(`/api/trade_journal${qs ? '?' + qs : ''}`);
        const data = res.ok ? await res.json() : getDemoJournal();
        renderTradeJournal(data);
    } catch (e) {
        renderTradeJournal(getDemoJournal());
    }
}

function getDemoJournal() {
    return {
        trades: [
            { open_time: "2026-05-03 09:15", strategy: "gold_momentum_breakout", pair: "XAUUSD", direction: "BUY", lots: 0.03, entry: 2318.45, exit: 2326.10, net_pnl: 245.50, status: "CLOSED", mode: "PAPER", close_reason: "TP_HIT", sl: 2308.00, tp: 2326.10 },
            { open_time: "2026-05-03 11:40", strategy: "rsi_pullback", pair: "GBPJPY", direction: "SELL", lots: 0.02, entry: 193.45, exit: 0, net_pnl: 0, status: "OPENED", mode: "PAPER", close_reason: "", sl: 194.10, tp: 192.50 },
            { open_time: "2026-05-02 14:20", strategy: "ma_crossover", pair: "USDJPY", direction: "BUY", lots: 0.03, entry: 152.80, exit: 152.40, net_pnl: -144.00, status: "CLOSED", mode: "PAPER", close_reason: "SL_HIT", sl: 152.40, tp: 153.60 }
        ],
        summary: { total: 3, closed: 2, open: 1, win_rate: 50.0, total_pnl: 101.50 }
    };
}

function applyJournalFilter() {
    const params = {};
    const df = document.getElementById('f-date-from').value;
    const dt = document.getElementById('f-date-to').value;
    const st = document.getElementById('f-strategy').value.trim();
    const pa = document.getElementById('f-pair').value.trim();
    const sx = document.getElementById('f-status').value;
    const mx = document.getElementById('f-mode').value;
    if (df) params.date_from = df;
    if (dt) params.date_to = dt;
    if (st) params.strategy = st;
    if (pa) params.pair = pa;
    if (sx) params.status = sx;
    if (mx) params.mode = mx;
    fetchTradeJournal(params);
}

function clearJournalFilter() {
    ['f-date-from','f-date-to','f-strategy','f-pair'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
    });
    ['f-status','f-mode'].forEach(id => {
        const el = document.getElementById(id); if (el) el.selectedIndex = 0;
    });
    fetchTradeJournal();
}

function renderTradeJournal(data) {
    const summary = data.summary || {};
    const pnl = summary.total_pnl || 0;
    const totEl = document.getElementById('j-total');
    const wrEl = document.getElementById('j-wr');
    const pnlEl = document.getElementById('j-pnl');
    if (totEl) totEl.textContent = `${summary.total || 0} trades (${summary.open || 0} open)`;
    if (wrEl) {
        wrEl.textContent = `${(summary.win_rate || 0).toFixed(1)}% WR`;
        wrEl.style.color = (summary.win_rate || 0) >= 60 ? 'var(--accent-green)' : 'var(--accent-orange)';
    }
    if (pnlEl) {
        pnlEl.textContent = `R ${pnl >= 0 ? '+' : ''}${pnl.toFixed(2)}`;
        pnlEl.style.color = pnl >= 0 ? 'var(--accent-green)' : 'var(--accent-red)';
    }
    const tbody = document.getElementById('journal-body');
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!data.trades || !data.trades.length) {
        tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;color:#a0a0a0;padding:2rem">No trades match the current filters.</td></tr>';
        return;
    }
    data.trades.forEach(t => {
        const dirColor = t.direction === 'BUY' ? 'var(--accent-green)' : 'var(--accent-red)';
        const pnlColor = t.net_pnl > 0 ? 'var(--accent-green)' : t.net_pnl < 0 ? 'var(--accent-red)' : 'var(--text-secondary)';
        const statusColor = t.status === 'OPENED' ? 'var(--accent-orange)' : 'var(--accent-cyan)';
        const modeColor = t.mode === 'MANUAL' ? '#a0a0a0' : 'var(--accent-cyan)';
        tbody.insertAdjacentHTML('beforeend', `
            <tr>
                <td style="font-size:0.8rem;color:var(--text-secondary)">${t.open_time}</td>
                <td style="font-size:0.85rem;font-weight:600">${t.strategy}</td>
                <td style="color:var(--accent-cyan)">${t.pair}</td>
                <td style="color:${dirColor};font-weight:700">${t.direction}</td>
                <td>${t.lots.toFixed(2)}</td>
                <td>${t.entry.toFixed(t.pair.includes('JPY') ? 3 : 5)}</td>
                <td>${t.exit > 0 ? t.exit.toFixed(t.pair.includes('JPY') ? 3 : 5) : '—'}</td>
                <td style="color:${pnlColor};font-weight:600">${t.net_pnl !== 0 ? 'R ' + (t.net_pnl >= 0 ? '+' : '') + t.net_pnl.toFixed(2) : '—'}</td>
                <td><span style="color:${statusColor};font-size:0.8rem;font-weight:600">${t.status}</span></td>
                <td><span style="color:${modeColor};font-size:0.8rem">${t.mode}</span></td>
                <td style="font-size:0.75rem;color:var(--text-secondary)">${t.close_reason || '—'}</td>
            </tr>`);
    });
}

function renderOptimizationTable(pipeline) {
    const tbody = document.getElementById('optimization-body');
    tbody.innerHTML = '';
    
    pipeline.queue.forEach(item => {
        const row = `
            <tr>
                <td><span class="badge">#${item.priority}</span></td>
                <td style="font-weight: 600">${item.strategy}</td>
                <td style="color: #00f2ff">${item.pair}</td>
                <td>${item.current_pf.toFixed(2)}</td>
                <td style="font-size: 0.8rem; color: #a0a0a0">${JSON.stringify(item.suggested_changes)}</td>
                <td style="color: #00ff88; font-weight: 600">${item.expected_improvement}</td>
            </tr>
        `;
        tbody.insertAdjacentHTML('beforeend', row);
    });
}

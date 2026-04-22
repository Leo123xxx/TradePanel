import React, { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const [logs, setLogs] = useState([])
  const [status, setStatus] = useState('CONNECTING')
  const terminalRef = useRef(null)
  const socketRef = useRef(null)

  useEffect(() => {
    // Fetch initial logs
    fetch('http://localhost:8000/api/logs')
      .then(res => res.json())
      .then(data => setLogs(data.reverse()))
      .catch(err => console.error('Failed to fetch logs:', err))

    // Connect to WebSocket
    const connect = () => {
      const ws = new WebSocket('ws://localhost:8000/ws/logs')
      socketRef.current = ws

      ws.onopen = () => setStatus('CONNECTED')
      ws.onmessage = (event) => {
        const newLog = JSON.parse(event.data)
        setLogs(prev => [...prev, newLog].slice(-200)) // Keep last 200
      }
      ws.onclose = () => {
        setStatus('DISCONNECTED')
        setTimeout(connect, 3000) // Reconnect after 3s
      }
    }

    connect()
    return () => socketRef.current?.close()
  }, [])

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [logs])

  return (
    <div className="dashboard">
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <h2 style={{ color: 'var(--accent-primary)', fontWeight: 800 }}>TRADEPANEL</h2>
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>HUB v1.0</span>
        </div>
        <div className="status-badge">
          <div className={`pulse ${status === 'CONNECTED' ? '' : 'offline'}`} style={{ backgroundColor: status === 'CONNECTED' ? 'var(--success)' : 'var(--critical)' }}></div>
          {status}
        </div>
      </header>

      <aside className="sidebar">
        <div className="card">
          <h4 style={{ marginBottom: '1rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>CONNECTIVITY</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>MT5 Bridge</span>
              <span style={{ color: 'var(--success)' }}>ONLINE</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>PostgreSQL</span>
              <span style={{ color: 'var(--success)' }}>READY</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span>Event Bus</span>
              <span style={{ color: 'var(--accent-primary)' }}>ACTIVE</span>
            </div>
          </div>
        </div>
        
        <div className="card">
          <h4 style={{ marginBottom: '1rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>QUICK ACTIONS</h4>
          <button style={{ width: '100%', padding: '8px', background: 'var(--accent-secondary)', border: 'none', borderRadius: '4px', color: 'white', cursor: 'pointer', fontWeight: 600 }}>
            RUN BACKTEST
          </button>
        </div>
      </aside>

      <main className="main-content">
        <section className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3>SYSTEM LOG PUBLICATION</h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{logs.length} events in buffer</span>
          </div>
          <div className="terminal" ref={terminalRef}>
            {logs.map((log, i) => (
              <div key={i} className="log-entry">
                <span className="log-time">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
                <span className={`log-type type-${log.event_type}`}>{log.event_type}</span>
                <span className="log-msg" style={{ color: log.status === 'CRITICAL' ? 'var(--critical)' : 'inherit' }}>
                  {log.message}
                  {log.meta_data && <span style={{ color: 'var(--text-secondary)', marginLeft: '8px', fontSize: '0.75rem' }}>
                    {JSON.stringify(log.meta_data)}
                  </span>}
                </span>
              </div>
            ))}
          </div>
        </section>

        <section style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
          <div className="card">
            <h3>ACTIVE STRATEGIES</h3>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>Monitor your bot's live decision making.</p>
          </div>
          <div className="card">
            <h3>RESEARCH ARCHIVE</h3>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>D:\Trade_training_data</p>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App

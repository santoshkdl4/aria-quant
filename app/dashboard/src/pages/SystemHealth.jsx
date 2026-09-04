import React, { useEffect, useState } from 'react'
import { Server, Cpu, Database, HardDrive, Clock, Loader2 } from 'lucide-react'

export default function SystemHealth() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        // Assume API is on 8000
        const res = await fetch('http://localhost:8000/api/system/health')
        if (!res.ok) throw new Error('API Error')
        const data = await res.json()
        setHealth(data)
        setError(null)
      } catch (err) {
        setError('Failed to connect to backend.')
      } finally {
        setLoading(false)
      }
    }

    fetchHealth()
    const interval = setInterval(fetchHealth, 5000) // Poll every 5s
    return () => clearInterval(interval)
  }, [])

  if (loading && !health) {
    return <div className="flex h-full items-center justify-center text-gray-500"><Loader2 className="animate-spin mr-2" /> Loading...</div>
  }

  if (error && !health) {
    return <div className="p-4 bg-aria-red/20 border border-aria-red/50 text-aria-red rounded-lg">{error}</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">System Health</h2>
        <p className="text-gray-400 mt-1">Real-time status of the ARIA QUANT backend engine.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <HealthCard 
          title="CPU Usage" 
          value={`${health?.cpu_percent.toFixed(1) || 0}%`}
          icon={<Cpu size={24} className="text-aria-cyan" />}
          status={health?.cpu_percent > 85 ? 'warning' : 'ok'}
        />
        <HealthCard 
          title="Memory Usage" 
          value={`${health?.memory_percent.toFixed(1) || 0}%`}
          subValue={`${health?.memory_used_mb.toFixed(0) || 0} MB`}
          icon={<Server size={24} className="text-aria-cyan" />}
          status={health?.memory_percent > 85 ? 'warning' : 'ok'}
        />
        <HealthCard 
          title="Disk Free" 
          value={`${health?.disk_free_gb.toFixed(1) || 0} GB`}
          icon={<HardDrive size={24} className="text-aria-cyan" />}
          status={health?.disk_free_gb < 10 ? 'warning' : 'ok'}
        />
        <HealthCard 
          title="Uptime" 
          value={`${formatUptime(health?.uptime_seconds || 0)}`}
          icon={<Clock size={24} className="text-aria-cyan" />}
          status="ok"
        />
      </div>
      
      <div className="mt-8 bg-aria-card border border-aria-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <Database size={20} className="mr-2 text-gray-400" /> Database Status
        </h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center py-2 border-b border-gray-800">
            <span className="text-gray-300">aria_state.db (SQLite)</span>
            <span className="px-2 py-1 rounded bg-aria-green/20 text-aria-green text-xs font-medium">ONLINE</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-gray-800">
            <span className="text-gray-300">aria_memory.db (SQLite)</span>
            <span className="px-2 py-1 rounded bg-aria-green/20 text-aria-green text-xs font-medium">ONLINE</span>
          </div>
          <div className="flex justify-between items-center py-2">
            <span className="text-gray-300">aria_market_data (DuckDB)</span>
            <span className="px-2 py-1 rounded bg-gray-800 text-gray-400 text-xs font-medium">PENDING INIT</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function HealthCard({ title, value, subValue, icon, status }) {
  const isWarning = status === 'warning'
  return (
    <div className={`p-6 rounded-lg border ${isWarning ? 'bg-aria-amber/10 border-aria-amber/50' : 'bg-aria-card border-aria-border'} shadow-sm`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-400">{title}</p>
          <div className="mt-2 flex items-baseline gap-2">
            <p className={`text-3xl font-bold ${isWarning ? 'text-aria-amber' : 'text-white'}`}>{value}</p>
            {subValue && <span className="text-sm text-gray-500">{subValue}</span>}
          </div>
        </div>
        <div className={`p-3 rounded-xl ${isWarning ? 'bg-aria-amber/20 text-aria-amber' : 'bg-aria-border text-gray-300'}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function formatUptime(seconds) {
  if (!seconds) return '0s'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  if (h > 0) return `${h}h ${m}m`
  if (m > 0) return `${m}m ${s}s`
  return `${s}s`
}

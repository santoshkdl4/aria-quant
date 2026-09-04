import React from 'react'
import { Activity, BrainCircuit, Terminal as TerminalIcon, TrendingUp } from 'lucide-react'
import CommandTerminal from '../components/CommandTerminal'
import PortfolioChart from '../components/PortfolioChart'

export default function DashboardHome() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Header Section */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">ARIA QUANT <span className="text-aria-cyan font-light">Laboratory</span></h1>
          <p className="text-gray-400 mt-2">Autonomous Research & Investment AI</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-400 bg-aria-card px-4 py-2 rounded-full border border-aria-border">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-aria-cyan opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-aria-cyan"></span>
          </span>
          <span>System Online</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* ARIA Face Component */}
        <div className="lg:col-span-1 bg-aria-card border border-aria-border rounded-xl p-8 flex flex-col items-center justify-center relative overflow-hidden shadow-lg">
          {/* Subtle background glow */}
          <div className="absolute inset-0 bg-aria-cyan/5 blur-3xl rounded-full scale-150 transform -translate-y-1/2"></div>
          
          <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-8 z-10">AI Core Status</h3>
          
          <div className="relative z-10 w-48 h-48 flex items-center justify-center">
            {/* Pulsing rings */}
            <div className="absolute inset-0 rounded-full border border-aria-cyan/20 animate-[spin_10s_linear_infinite]"></div>
            <div className="absolute inset-2 rounded-full border-t border-r border-aria-cyan/40 animate-[spin_7s_linear_infinite_reverse]"></div>
            <div className="absolute inset-6 rounded-full border-b border-l border-aria-cyan/30 animate-[spin_4s_linear_infinite]"></div>
            
            {/* Core Orb */}
            <div className="absolute inset-10 rounded-full bg-gradient-to-br from-aria-cyan to-blue-600 shadow-[0_0_40px_rgba(34,211,238,0.5)] animate-pulse-slow"></div>
            
            {/* Core Icon */}
            <BrainCircuit className="relative z-20 text-white" size={40} />
          </div>

          <div className="mt-8 text-center z-10">
            <p className="text-xl font-bold text-white mb-1">Idle / Ready</p>
            <p className="text-sm text-gray-400">Awaiting Research Directives</p>
          </div>
        </div>

        {/* Quick Actions / Activity Feed */}
        <div className="lg:col-span-2 space-y-8">
          <div className="grid grid-cols-1 gap-4">
            <PortfolioChart />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-8">
            <ActionCard icon={<TrendingUp size={20} />} title="Backtest" desc="Historical Data" />
            <ActionCard icon={<Activity size={20} />} title="Live Trade" desc="Paper execution" />
            <ActionCard icon={<TerminalIcon size={20} />} title="Logs" desc="System traces" />
            <ActionCard icon={<BrainCircuit size={20} />} title="Research" desc="AI Hypotheses" />
          </div>

          <CommandTerminal />
        </div>
        
      </div>
    </div>
  )
}

function ActionCard({ icon, title, desc }) {
  return (
    <button className="flex flex-col items-start p-6 bg-aria-card border border-aria-border rounded-xl hover:bg-aria-card-hover hover:border-aria-cyan/50 transition-all duration-300 text-left group">
      <div className="p-3 bg-aria-bg rounded-lg text-aria-cyan mb-4 group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h4 className="text-white font-medium text-lg">{title}</h4>
      <p className="text-gray-400 text-sm mt-1">{desc}</p>
    </button>
  )
}

function ActivityRow({ time, message, type }) {
  const colors = {
    system: 'text-gray-400',
    success: 'text-aria-green',
    info: 'text-aria-cyan',
    error: 'text-aria-red'
  }
  return (
    <div className="flex items-start space-x-3 text-sm">
      <span className="text-gray-500 whitespace-nowrap">{time}</span>
      <span className={`font-mono ${colors[type]}`}>&gt; {message}</span>
    </div>
  )
}

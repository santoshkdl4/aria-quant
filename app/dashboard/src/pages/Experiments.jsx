import React from 'react'
import { TestTube } from 'lucide-react'

export default function Experiments() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Experiments</h1>
          <p className="text-gray-400 mt-2">Active algorithms and backtest results</p>
        </div>
      </div>
      
      <div className="bg-aria-card border border-aria-border rounded-xl p-6 h-96 flex flex-col items-center justify-center">
        <TestTube className="text-gray-600 mb-4" size={48} />
        <p className="text-gray-400">No active experiments running.</p>
        <p className="text-sm text-gray-500 mt-2">Generate a strategy using the AI Brain to see it here.</p>
      </div>
    </div>
  )
}

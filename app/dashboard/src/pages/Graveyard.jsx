import React from 'react'
import { Cross } from 'lucide-react'

export default function Graveyard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Strategy Graveyard</h1>
          <p className="text-gray-400 mt-2">Failed algorithms and rejected hypotheses</p>
        </div>
      </div>
      
      <div className="bg-aria-card border border-aria-border rounded-xl p-6 h-96 flex flex-col items-center justify-center">
        <Cross className="text-gray-600 mb-4" size={48} />
        <p className="text-gray-400">The graveyard is empty.</p>
        <p className="text-sm text-gray-500 mt-2">Algorithms that fail verification tests will be archived here.</p>
      </div>
    </div>
  )
}

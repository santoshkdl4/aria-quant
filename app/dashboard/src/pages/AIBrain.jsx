import React from 'react'
import { BrainCircuit } from 'lucide-react'
import CommandTerminal from '../components/CommandTerminal'

export default function AIBrain() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">AI Brain</h1>
          <p className="text-gray-400 mt-2">Agentic Research & Strategy Generation</p>
        </div>
      </div>
      
      <div className="bg-aria-card border border-aria-border rounded-xl p-6">
        <div className="flex items-center space-x-3 mb-6">
          <BrainCircuit className="text-aria-cyan" size={24} />
          <h2 className="text-lg font-medium text-white">Neural Command Interface</h2>
        </div>
        <p className="text-gray-400 mb-6">
          Issue natural language prompts to the AI quant agent. For example, "Backtest a moving average crossover on RELIANCE".
        </p>
        <CommandTerminal />
      </div>
    </div>
  )
}

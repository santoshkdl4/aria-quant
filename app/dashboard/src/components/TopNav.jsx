import React from 'react'

export default function TopNav() {
  return (
    <header className="h-16 flex-shrink-0 border-b border-aria-border bg-aria-card flex items-center justify-between px-6">
      <div className="flex items-center">
        <div className="px-3 py-1 rounded bg-aria-border text-xs font-medium text-gray-400 mr-4 shadow-sm border border-gray-700">
          MARKET: <span className="text-aria-green">CLOSED</span>
        </div>
        <div className="px-3 py-1 rounded border border-aria-amber/30 bg-aria-amber/10 text-aria-amber text-xs font-bold tracking-wide">
          PAPER TRADING MODE - ₹10,00,000 VIRTUAL
        </div>
      </div>
      
      <div className="flex items-center space-x-4 text-sm text-gray-400">
        <div className="flex items-center">
          <span className="w-2 h-2 rounded-full bg-aria-green mr-2 shadow-[0_0_8px_#10b981]"></span>
          Connected
        </div>
      </div>
    </header>
  )
}

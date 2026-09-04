import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useStore } from '../store/useStore'

export default function PortfolioChart() {
  const { livePrices } = useStore()
  
  // For demonstration, we'll map the live prices to a simple format for Recharts
  // A real app would maintain a time-series history array in the store
  const data = Object.keys(livePrices).map(symbol => ({
    name: symbol,
    price: livePrices[symbol]
  }))
  
  if (data.length === 0) {
    return (
      <div className="bg-aria-card border border-aria-border rounded-xl p-6 h-64 flex items-center justify-center">
        <p className="text-gray-500">Waiting for live market data...</p>
      </div>
    )
  }

  return (
    <div className="bg-aria-card border border-aria-border rounded-xl p-6 h-80">
      <h3 className="text-white font-medium mb-4">Live Market Prices</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" />
          <XAxis dataKey="name" stroke="#888" />
          <YAxis stroke="#888" domain={['auto', 'auto']} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #333' }}
            itemStyle={{ color: '#00F0FF' }}
          />
          <Line type="monotone" dataKey="price" stroke="#00F0FF" strokeWidth={2} activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

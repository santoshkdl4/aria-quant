import React from 'react'
import { Settings as SettingsIcon } from 'lucide-react'

export default function Settings() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">System Settings</h1>
          <p className="text-gray-400 mt-2">Configure keys, environment, and risk limits</p>
        </div>
      </div>
      
      <div className="bg-aria-card border border-aria-border rounded-xl p-6">
        <div className="space-y-6">
          <div>
            <h3 className="text-white font-medium mb-4 flex items-center"><SettingsIcon size={18} className="mr-2 text-aria-cyan"/> API Keys</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Google GenAI Key (Gemini)</label>
                <input type="password" placeholder="************************" className="w-full max-w-md bg-aria-bg border border-aria-border rounded-md px-3 py-2 text-white focus:outline-none focus:border-aria-cyan" readOnly />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Broker API Key (Paper)</label>
                <input type="password" placeholder="************************" className="w-full max-w-md bg-aria-bg border border-aria-border rounded-md px-3 py-2 text-white focus:outline-none focus:border-aria-cyan" readOnly />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

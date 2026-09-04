import React from 'react'
import { NavLink } from 'react-router-dom'
import { LayoutDashboard, BrainCircuit, Activity, TestTube, Cross, Settings } from 'lucide-react'

export default function Sidebar() {
  return (
    <div className="w-64 flex-shrink-0 border-r border-aria-border bg-aria-card flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-aria-border">
        <h1 className="text-xl font-bold tracking-wider text-white">ARIA <span className="text-aria-cyan">QUANT</span></h1>
      </div>
      
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          <SectionTitle>OVERVIEW</SectionTitle>
          <NavItem to="/dashboard" icon={<LayoutDashboard size={18} />}>Dashboard</NavItem>
          <NavItem to="/brain" icon={<BrainCircuit size={18} />}>AI Brain</NavItem>
          
          <SectionTitle>RESEARCH LAB</SectionTitle>
          <NavItem to="/experiments" icon={<TestTube size={18} />}>Experiments</NavItem>
          <NavItem to="/graveyard" icon={<Cross size={18} />}>Graveyard</NavItem>
          
          <SectionTitle>SYSTEM</SectionTitle>
          <NavItem to="/system" icon={<Activity size={18} />}>System Health</NavItem>
          <NavItem to="/settings" icon={<Settings size={18} />}>Settings</NavItem>
        </nav>
      </div>
    </div>
  )
}

function SectionTitle({ children }) {
  return (
    <h3 className="px-3 pt-4 pb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
      {children}
    </h3>
  )
}

function NavItem({ to, icon, children }) {
  return (
    <NavLink 
      to={to} 
      className={({ isActive }) => 
        `flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
          isActive 
            ? 'bg-aria-border text-white' 
            : 'text-gray-400 hover:bg-gray-800 hover:text-white'
        }`
      }
    >
      <span className="mr-3">{icon}</span>
      {children}
    </NavLink>
  )
}

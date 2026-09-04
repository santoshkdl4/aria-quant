import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardHome from './pages/DashboardHome'
import SystemHealth from './pages/SystemHealth'
import AIBrain from './pages/AIBrain'
import Experiments from './pages/Experiments'
import Graveyard from './pages/Graveyard'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardHome />} />
          <Route path="brain" element={<AIBrain />} />
          <Route path="experiments" element={<Experiments />} />
          <Route path="graveyard" element={<Graveyard />} />
          <Route path="system" element={<SystemHealth />} />
          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<div className="p-8 text-center text-gray-500">Not Implemented Yet</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

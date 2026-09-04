import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardHome from './pages/DashboardHome'
import SystemHealth from './pages/SystemHealth'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardHome />} />
          <Route path="system" element={<SystemHealth />} />
          <Route path="*" element={<div className="p-8 text-center text-gray-500">Not Implemented Yet</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

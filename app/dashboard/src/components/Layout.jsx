import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopNav from './TopNav'

export default function Layout() {
  return (
    <div className="flex h-screen overflow-hidden bg-aria-bg">
      <Sidebar />
      <div className="flex flex-col flex-1 w-full overflow-hidden">
        <TopNav />
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

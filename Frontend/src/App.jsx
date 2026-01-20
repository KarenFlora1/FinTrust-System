import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from './components/Navbar'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="container mx-auto max-w-5xl w-full flex-1 py-8">
        <Outlet />
      </main>
      <footer className="py-6 text-center text-sm text-gray-500">
        FinTrust • {new Date().getFullYear()}
      </footer>
    </div>
  )
}

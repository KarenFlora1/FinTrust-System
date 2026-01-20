import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')

  function handleLogout() {
    localStorage.removeItem('token')
    navigate('/')
  }

  return (
    <header className="sticky top-0 z-10 border-b bg-white/80 backdrop-blur">
      <div className="container mx-auto max-w-5xl flex h-14 items-center justify-between">
        <Link to="/" className="font-semibold tracking-tight text-sky-700">
          FinTrust
        </Link>
        <nav className="flex items-center gap-3 text-sm">
          {token ? (
            <>
              <Link className="hover:underline" to="/dashboard">Dashboard</Link>
              <button onClick={handleLogout} className="btn-muted">Sair</button>
            </>
          ) : (
            <Link className="btn-primary" to="/">Entrar</Link>
          )}
        </nav>
      </div>
    </header>
  )
}

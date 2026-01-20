import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../lib/api'

export default function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function onSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const data = await login(username, password)
      // Expecting {token: '...'} from backend
      const token = data.token || data?.access_token
      if (!token) throw new Error('Token não retornado pelo servidor')
      localStorage.setItem('token', token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message || 'Credenciais inválidas')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card p-6">
        <h1 className="text-2xl font-semibold mb-2">Entrar</h1>
        <p className="text-sm text-gray-500 mb-6">Autentique-se para aceder ao painel.</p>
        <form className="space-y-4" onSubmit={onSubmit}>
          <div className="space-y-1">
            <label className="text-sm font-medium">Utilizador</label>
            <input className="field" value={username} onChange={e=>setUsername(e.target.value)} placeholder="nome" required />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium">Palavra-passe</label>
            <input className="field" type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="••••••••" required />
          </div>
          {error && <div className="text-sm text-red-600">{error}</div>}
          <button className="btn-primary w-full" disabled={loading}>{loading ? 'A entrar…' : 'Entrar'}</button>
        </form>
      </div>
    </div>
  )
}

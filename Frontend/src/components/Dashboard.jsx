import React, { useEffect, useState, useCallback } from 'react'
import { listAccounts } from '../lib/api'
import AccountsList from './AccountsList'
import TransferForm from './TransferForm'
import History from './History'   // NOVO

export default function Dashboard() {
  const [accounts, setAccounts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const token = localStorage.getItem('token') || ''

  const fetchAccounts = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const data = await listAccounts(token)
      // Espera { accounts: [{id,balance}] }
      setAccounts(data.accounts || [])
    } catch (err) {
      setError(err.message || 'Erro ao carregar contas')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    fetchAccounts()
  }, [fetchAccounts])

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Painel</h1>
          <p className="text-sm text-gray-500">Veja as suas contas e realize transferências.</p>
        </div>
        <button onClick={fetchAccounts} className="btn-muted">Atualizar</button>
      </div>

      {loading ? (
        <div>Carregando…</div>
      ) : error ? (
        <div className="text-red-600">{error}</div>
      ) : (
        <>
          <AccountsList accounts={accounts} />
          <TransferForm accounts={accounts} onSuccess={fetchAccounts} />
          <History />  {/* NOVO: histórico abaixo do formulário */}
        </>
      )}
    </div>
  )
}

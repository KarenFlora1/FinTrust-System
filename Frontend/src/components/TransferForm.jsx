import React, { useState, useMemo } from 'react'
import { makeTransfer } from '../lib/api'

export default function TransferForm({ accounts = [], onSuccess }) {
  const [fromAccount, setFromAccount] = useState('')
  const [toAccount, setToAccount] = useState('')     // agora digitado
  const [amount, setAmount] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const token = localStorage.getItem('token') || ''

  const fromIdNum = useMemo(() => Number(fromAccount || 0), [fromAccount])
  const toIdNum   = useMemo(() => Number(toAccount || 0), [toAccount])
  const amtNum    = useMemo(() => Number(amount || 0), [amount])

  const canSubmit = useMemo(() => {
    if (!fromIdNum || !toIdNum || !amtNum) return false
    if (fromIdNum === toIdNum) return false
    if (amtNum <= 0) return false
    return true
  }, [fromIdNum, toIdNum, amtNum])

  async function onSubmit(e) {
    e.preventDefault()
    setError('')

    // validações rápidas no cliente
    if (!fromIdNum || !toIdNum || !amtNum) {
      setError('Preencha todos os campos.')
      return
    }
    if (fromIdNum === toIdNum) {
      setError('Conta de origem e destino devem ser diferentes.')
      return
    }
    if (amtNum <= 0) {
      setError('Montante deve ser maior que zero.')
      return
    }

    setLoading(true)
    try {
      const payload = {
        from_account: fromIdNum,
        to_account: toIdNum,
        amount: amtNum
      }
      await makeTransfer(token, payload)
      // limpa somente o montante e o destino (mantém a origem selecionada para facilitar)
      setToAccount('')
      setAmount('')
      if (onSuccess) onSuccess()
    } catch (err) {
      setError(err.message || 'Falha na transferência')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={onSubmit} className="card p-4 space-y-3">
      <h3 className="text-lg font-semibold">Transferir</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* ORIGEM: mantém select apenas com as SUAS contas */}
        <div>
          <label className="text-sm font-medium">De</label>
          <select
            className="field"
            value={fromAccount}
            onChange={e => setFromAccount(e.target.value)}
            required
          >
            <option value="" disabled>Selecione</option>
            {accounts.map(a => {
              const id = a.id ?? a.account_id
              return (
                <option key={id} value={id}>#{id}</option>
              )
            })}
          </select>
        </div>

        {/* DESTINO: input para digitar o ID da conta destino */}
        <div>
          <label className="text-sm font-medium">Para</label>
          <input
            className="field"
            type="number"
            inputMode="numeric"
            min="1"
            placeholder="ID da conta destino (ex.: 3)"
            value={toAccount}
            onChange={e => setToAccount(e.target.value)}
            required
          />
          <p className="mt-1 text-xs text-gray-500">
            Digite o ID da conta destino. Pode ser de outro utilizador.
          </p>
        </div>

        {/* MONTANTE */}
        <div>
          <label className="text-sm font-medium">Montante</label>
          <input
            className="field"
            type="number"
            step="0.01"
            min="0.01"
            value={amount}
            onChange={e => setAmount(e.target.value)}
            placeholder="0.00"
            required
          />
        </div>
      </div>

      {error && <div className="text-sm text-red-600">{error}</div>}

      <button
        className="btn-primary"
        disabled={loading || !canSubmit}
      >
        {loading ? 'A transferir…' : 'Confirmar'}
      </button>
    </form>
  )
}

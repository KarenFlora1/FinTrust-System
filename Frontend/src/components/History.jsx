import React, { useEffect, useState } from 'react'
import { listHistory } from '../lib/api'

export default function History() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const token = localStorage.getItem('token') || ''

  async function load() {
    setLoading(true); setError('')
    try {
      const data = await listHistory(token, 50)
      setItems(data.items || [])
    } catch (e) {
      setError(e.message || 'Erro ao carregar histórico')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold">Histórico de transferências</h3>
        <button className="btn-muted" onClick={load}>Atualizar</button>
      </div>

      {loading ? (
        <div>Carregando…</div>
      ) : error ? (
        <div className="text-red-600 text-sm">{error}</div>
      ) : items.length === 0 ? (
        <div className="text-gray-500 text-sm">Sem movimentos.</div>
      ) : (
        <div className="overflow-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500">
                <th className="py-2 pr-4">Data</th>
                <th className="py-2 pr-4">De</th>
                <th className="py-2 pr-4">Para</th>
                <th className="py-2 pr-4">Montante</th>
              </tr>
            </thead>
            <tbody>
              {items.map((it, idx) => (
                <tr key={idx} className="border-t">
                  <td className="py-2 pr-4">{new Date(it.ts).toLocaleString()}</td>
                  <td className="py-2 pr-4">#{it.from_account}</td>
                  <td className="py-2 pr-4">#{it.to_account}</td>
                  <td className="py-2 pr-4 font-medium">
                    {Number(it.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} MTn
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

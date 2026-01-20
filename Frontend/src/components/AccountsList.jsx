import React from 'react'

export default function AccountsList({ accounts = [] }) {
  if (!accounts.length) {
    return <div className="text-gray-600">Sem contas para mostrar.</div>
  }
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {accounts.map(acc => (
        <div key={acc.id || acc.account_id} className="card p-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">Conta #{acc.id || acc.account_id}</h3>
            <span className="text-sm text-gray-500">Utilizador: {acc.user_id ?? '—'}</span>
          </div>
          <div className="mt-2 text-2xl font-bold">
            {Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(acc.balance)}
          </div>
        </div>
      ))}
    </div>
  )
}

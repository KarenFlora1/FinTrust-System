# FinTrust Frontend (Vite + React + Tailwind)

Frontend simples para autenticação, listagem de contas e transferências,
integrado ao **API Gateway** FastAPI (porta `8080`) do projeto FinTrust.

## Requisitos
- Node.js 18+ (recomendado 20+)
- Backend em execução (Auth/Accounts/Transfers + Gateway).

## Instalação
```bash
npm i
cp .env.example .env    # ajuste se necessário
npm run dev
```

## Endpoints esperados do backend
- `POST /login` → `{ token }`
- `GET /accounts` (Auth: Bearer) → `{ accounts: [{ id, balance }] }`
- `POST /transfer` (Auth: Bearer) → body `{ from_account, to_account, amount }`

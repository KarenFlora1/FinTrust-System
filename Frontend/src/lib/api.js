// src/lib/api.js — versão com histórico
console.log("🌐 API_BASE usado =", import.meta.env.VITE_API_BASE || "http://127.0.0.1:8080");
const API_BASE = (import.meta.env.VITE_API_BASE || "http://127.0.0.1:8080").replace(/\/+$/, "");

async function http(path, { method = "GET", token, json, headers = {} } = {}) {
  const h = { ...headers };
  if (json !== undefined) h["Content-Type"] = "application/json";
  if (token)
    h["Authorization"] = token.toLowerCase().startsWith("bearer ")
      ? token
      : `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: h,
    body: json !== undefined ? JSON.stringify(json) : undefined,
  });

  if (!res.ok) {
    let msg = "";
    try {
      const data = await res.json();
      msg = data?.detail || data?.message || "";
    } catch {
      try { msg = await res.text(); } catch { msg = ""; }
    }
    throw new Error(msg || `Erro ${res.status}`);
  }

  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? res.json() : res.text();
}

export const login        = (u, p)       => http("/login",    { method: "POST", json: { username: u, password: p } });
export const listAccounts = (t)          => http("/accounts", { token: t });
export const makeTransfer = (t, payload) => http("/transfer", { method: "POST", token: t, json: payload });
// NOVO: histórico
export const listHistory  = (t, limit=50)=> http(`/history?limit=${encodeURIComponent(limit)}`, { token: t });

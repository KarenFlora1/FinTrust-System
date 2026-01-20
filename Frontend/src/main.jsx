import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import App from './App'
import LoginForm from './components/LoginForm'
import Dashboard from './components/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'

const router = createBrowserRouter([
  { path: '/', element: <App />,
    children: [
      { index: true, element: <LoginForm /> },
      { path: 'dashboard', element: (
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
      )},
    ]
  },
])

const root = createRoot(document.getElementById('root'))
root.render(<RouterProvider router={router} />)

'use client'

import { useState, useEffect } from 'react'

export default function ApiExample() {
  const [apiMessage, setApiMessage] = useState<string>('Loading...')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchApiExample = async () => {
      try {
        const backendHost = process.env.NEXT_PUBLIC_BACKEND_HOST || 'localhost'
        const backendPort = process.env.NEXT_PUBLIC_BACKEND_PORT || '8000'
        const response = await fetch(`http://${backendHost}:${backendPort}/api/example`)

        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}`)
        }

        const data = await response.json()
        setApiMessage(data.message)
        setError(null)
      } catch (err) {
        console.error('Error fetching API example:', err)
        setApiMessage('Failed to load')
        setError(err instanceof Error ? err.message : 'Unknown error')
      }
    }

    fetchApiExample()
  }, [])

  return (
    <div className="w-full max-w-md p-6 border rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">API Connection Example</h2>
      <div className="mb-2">
        <p className="text-sm font-medium">Message from API:</p>
        <p className="p-2 bg-gray-100 rounded">{apiMessage}</p>
      </div>
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded">
          <p className="font-medium">Error:</p>
          <p className="text-sm">{error}</p>
        </div>
      )}
    </div>
  )
}

import { useState } from 'react'
import { TestCard } from './components'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 space-y-6">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            🚀 Tailwind Test
          </h1>
          <p className="text-gray-600">
            Testing Tailwind CSS with Vite + React
          </p>
        </div>

        {/* Counter Card */}
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-6 text-white text-center">
          <h2 className="text-xl font-semibold mb-4">Counter Demo</h2>
          <div className="text-4xl font-bold mb-4">{count}</div>
          <button 
            onClick={() => setCount((count) => count + 1)}
            className="bg-white text-purple-600 px-6 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors duration-200 shadow-md"
          >
            Increment
          </button>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-2 gap-4">
          <TestCard 
            title="Tailwind CSS" 
            description="Styling working perfectly" 
            icon="✅" 
            color="green" 
          />
          <TestCard 
            title="Vite Build" 
            description="Fast development server" 
            icon="⚡" 
            color="blue" 
          />
        </div>

        {/* Reset Button */}
        <button 
          onClick={() => setCount(0)}
          className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 rounded-lg font-medium transition-colors duration-200"
        >
          Reset Counter
        </button>
      </div>
    </div>
  )
}

export default App

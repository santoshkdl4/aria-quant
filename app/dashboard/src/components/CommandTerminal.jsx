import React, { useState, useRef, useEffect } from 'react'
import { Send, Terminal } from 'lucide-react'
import { useStore } from '../store/useStore'

export default function CommandTerminal() {
  const { terminalMessages, sendTerminalCommand, connectWebSocket, isConnected } = useStore()
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    connectWebSocket()
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [terminalMessages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    sendTerminalCommand(input)
    setInput('')
  }

  return (
    <div className="bg-aria-card border border-aria-border rounded-xl flex flex-col h-[400px] overflow-hidden shadow-lg">
      <div className="px-4 py-3 border-b border-aria-border bg-aria-bg-darker flex items-center">
        <Terminal size={18} className="text-aria-cyan mr-2" />
        <h3 className="text-sm font-semibold text-white tracking-wide">ARIA Command Terminal</h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {terminalMessages.map(msg => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-lg p-3 text-sm ${
              msg.sender === 'user' 
                ? 'bg-aria-cyan/20 border border-aria-cyan/30 text-white rounded-br-none' 
                : 'bg-gray-800 border border-gray-700 text-gray-300 rounded-bl-none'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        {!isConnected && (
          <div className="flex justify-start">
            <div className="bg-red-900/30 border border-red-700/50 rounded-lg rounded-bl-none p-3 text-sm text-red-400">
              Connection lost. Attempting to reconnect...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="p-3 border-t border-aria-border bg-aria-bg-darker flex items-center">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Issue a command to ARIA..." 
          className="flex-1 bg-transparent text-white text-sm focus:outline-none placeholder-gray-600"
        />
        <button 
          type="submit" 
          disabled={!input.trim()}
          className="p-2 rounded-lg bg-aria-cyan/10 text-aria-cyan hover:bg-aria-cyan/20 disabled:opacity-50 transition-colors"
        >
          <Send size={16} />
        </button>
      </form>
    </div>
  )
}

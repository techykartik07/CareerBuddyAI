import { useState } from 'react'
import { sendChatMessage } from '../api/client'

export default function ChatPanel({ context }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hi! I am your CareerBuddy AI assistant. Ask me anything about your resume or career path.' }
  ])
  const [input,  setInput]   = useState('')
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setMessages(m => [...m, { role: 'user', text: userMsg }])
    setInput('')
    setLoading(true)
    try {
      const { reply } = await sendChatMessage(userMsg, context)
      setMessages(m => [...m, { role: 'assistant', text: reply }])
    } catch {
      setMessages(m => [...m, { role: 'assistant', text: 'Sorry, I could not respond. Please try again.' }])
    } finally { setLoading(false) }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm flex flex-col h-96">
      <div className="p-4 border-b border-gray-100">
        <h2 className="font-semibold text-gray-800">AI Career Assistant</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs px-4 py-2 rounded-2xl text-sm
              ${m.role === 'user'
                ? 'bg-purple-600 text-white rounded-br-sm'
                : 'bg-gray-100 text-gray-700 rounded-bl-sm'}`}>
              {m.text}
            </div>
          </div>
        ))}
        {loading && <div className="flex justify-start">
          <div className="bg-gray-100 px-4 py-2 rounded-2xl text-sm text-gray-400">Thinking...</div>
        </div>}
      </div>
      <div className="p-4 border-t border-gray-100 flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="Ask about your career..." className="flex-1 px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-purple-400" />
        <button onClick={send}
          className="px-4 py-2 bg-purple-600 text-white rounded-xl text-sm hover:bg-purple-700">
          Send
        </button>
      </div>
    </div>
  )
}
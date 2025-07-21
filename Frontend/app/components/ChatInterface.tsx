// ChatInterface.tsx

import React, { useState } from 'react';
import axios from 'axios';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  daxQuery?: string;
  data?: any[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(
        `http://localhost:8000/api/powerbi/query-natural`,
        { question: input }
      );

      const assistantMessage: Message = {
        id: messages.length + 2,
        text: response.data.response,
        sender: 'assistant',
        timestamp: new Date(),
        daxQuery: response.data.dax_query,
        data: response.data.execution?.rows || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: messages.length + 2,
          text: 'Error connecting to backend.',
          sender: 'assistant',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: 'auto' }}>
      <h2>💬 Power BI Chat Assistant (PPU)</h2>
      <div style={{ maxHeight: 400, overflowY: 'auto', border: '1px solid #ccc', padding: 10 }}>
        {messages.map((msg) => (
          <div key={msg.id} style={{ marginBottom: 15 }}>
            <strong>{msg.sender === 'user' ? 'You' : 'Assistant'}:</strong> {msg.text}
            {msg.daxQuery && (
              <pre style={{ background: '#f4f4f4', padding: 10, marginTop: 5 }}>
                {msg.daxQuery}
              </pre>
            )}
            {msg.data && msg.data.length > 0 && (
              <table style={{ border: '1px solid #ccc', marginTop: 10, width: '100%' }}>
                <thead>
                  <tr>
                    {Object.keys(msg.data[0]).map((col) => (
                      <th key={col} style={{ border: '1px solid #ccc', padding: 5 }}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {msg.data.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((val, i) => (
                        <td key={i} style={{ border: '1px solid #ccc', padding: 5 }}>{val as string}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        ))}
      </div>

      <div style={{ marginTop: 20 }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something like 'Top 5 cities by sales'"
          style={{ width: '80%', padding: 10, fontSize: 16 }}
        />
        <button onClick={sendMessage} disabled={loading} style={{ padding: 10, marginLeft: 10 }}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;

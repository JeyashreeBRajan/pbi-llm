'use client';

import { useState } from 'react';
import ConfigStatus from './components/ConfigStatus';
import SchemaExplorer from './components/SchemaExplorer';
import EnhancedChatInterface from './components/EnhancedChatInterface';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'schema'>('chat');

  return (
    <main style={{ 
      padding: '2rem', 
      maxWidth: '1400px', 
      margin: '0 auto',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <h1 style={{ marginBottom: '2rem', textAlign: 'center' }}>
        🤖 Power BI Copilot Chat
      </h1>

      <ConfigStatus />

      <div style={{ marginBottom: '1rem' }}>
        <button
          onClick={() => setActiveTab('chat')}
          style={{
            padding: '0.5rem 1rem',
            marginRight: '0.5rem',
            backgroundColor: activeTab === 'chat' ? '#007bff' : '#f8f9fa',
            color: activeTab === 'chat' ? 'white' : 'black',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Chat
        </button>
        <button
          onClick={() => setActiveTab('schema')}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: activeTab === 'schema' ? '#007bff' : '#f8f9fa',
            color: activeTab === 'schema' ? 'white' : 'black',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Schema Explorer
        </button>
      </div>

      <div style={{ marginTop: '2rem' }}>
        {activeTab === 'chat' && <EnhancedChatInterface />}
        {activeTab === 'schema' && <SchemaExplorer connected={true} />}
      </div>

      <div style={{ 
        marginTop: '2rem', 
        padding: '1rem',
        backgroundColor: '#e3f2fd',
        borderRadius: '8px'
      }}>
        <h3>Sample Questions:</h3>
        <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
          <li>Show total sales by city</li>
          <li>What is the total sales amount this year?</li>
          <li>Top 5 cities with highest sales</li>
          <li>List sales by region</li>
        </ul>
      </div>
    </main>
  );
}

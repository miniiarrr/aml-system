'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('');
  const [messages, setMessages] = useState<string[]>([]);

  const startWorkflow = async () => {
    try {
      const response = await axios.post('http://localhost:8000/workflow/start');
      setWorkflowId(response.data.workflow_id);
      setStatus('Started');
    } catch (error) {
      console.error('Error starting workflow:', error);
      setStatus('Error starting workflow');
    }
  };

  useEffect(() => {
    if (workflowId) {
      const eventSource = new EventSource(`http://localhost:8000/workflow/${workflowId}/events`);
      
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setStatus(data.status);
        setMessages(prev => [...prev, data.message]);
      };

      eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        eventSource.close();
      };

      return () => {
        eventSource.close();
      };
    }
  }, [workflowId]);

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">AML System</h1>
        
        <div className="mb-8">
          <button
            onClick={startWorkflow}
            disabled={!!workflowId}
            className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-400"
          >
            Start New Workflow
          </button>
        </div>

        {workflowId && (
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-2">Workflow ID:</h2>
            <p className="font-mono bg-gray-100 p-2 rounded">{workflowId}</p>
          </div>
        )}

        {status && (
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-2">Status:</h2>
            <p className="font-mono bg-gray-100 p-2 rounded">{status}</p>
          </div>
        )}

        {messages.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold mb-2">Messages:</h2>
            <div className="bg-gray-100 p-4 rounded">
              {messages.map((message, index) => (
                <p key={index} className="mb-2">{message}</p>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
} 
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // We'll add custom styles for the dark theme

function App() {
  const [prompt, setPrompt] = useState('');
  const [state, setState] = useState('default'); // 'default', 'waiting', 'completed', 'error'
  const [result, setResult] = useState('');

  const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
  };

  const handleSubmit = async () => {
    if (!prompt) return;
    setState('waiting');
    setResult('');

    try {
      // Send the prompt to the backend (FastAPI)
      const response = await axios.post('http://localhost:8000/start-job', { prompt });
      const jobId = response.data.id;

      // Start polling for job status
      pollJobStatus(jobId);
    } catch (error) {
      setState('error');
      console.error('Error submitting job:', error);
    }
  };

  const pollJobStatus = async (jobId) => {
    try {
      let jobComplete = false;
      while (!jobComplete) {
        const response = await axios.get(`http://localhost:8000/job-status/${jobId}`);

        if (response.data.status === 'COMPLETED') {
          setState('completed');
          setResult(response.data.output[0].image);
          jobComplete = true;
        } else if (response.data.status === 'ERROR') {
          setState('error');
          console.error('Job encountered an error:', response.data.error);
          jobComplete = true;
        } else {
          // Delay for 2 seconds before polling again to avoid too many requests
          await sleep(2000);
        }
      }
    } catch (error) {
      setState('error');
      console.error('Error polling job status:', error);
    }
  };

  return (
    <div className="App">
      <h1>LLM Job Simulator</h1>
      <div className="input-container">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt"
        />
        <button onClick={handleSubmit}>Submit</button>
      </div>

      {state === 'waiting' && <div className="spinner">⏳ Waiting for results...</div>}
      {state === 'completed' && <div className="result">{result}</div>}
      {state === 'error' && <div className="error">Something went wrong. Please try again.</div>}
    </div>
  );
}

export default App;


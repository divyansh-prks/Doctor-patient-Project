// src/App.jsx
import { useState, useRef } from 'react';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [response, setResponse] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;
    audioChunksRef.current = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });

      const formData = new FormData();
      formData.append('audio', audioBlob, 'voice.wav');
    
      try {
        const res = await fetch('http://localhost:8000/api/voice-to-text/', {
          method: 'POST',
          body: formData,
        });
    
        const data = await res.json();
        setResponse(data.text || 'No response');
    
        // Speak it out loud!
        const utterance = new SpeechSynthesisUtterance(data.text);
        window.speechSynthesis.speak(utterance);
    
      } catch (error) {
        console.error(error);
        setResponse('Error occurred');
      }
    };

    mediaRecorder.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>🩺 Voice to Text Doctor</h1>
      <button onClick={startRecording} disabled={isRecording}>
        🎙️ Start Recording
      </button>
      <button onClick={stopRecording} disabled={!isRecording} style={{ marginLeft: '10px' }}>
        ⏹️ Stop & Send
      </button>

      <audio controls>
        <source src="http://localhost:8000/media/audio/advice.mp3" type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
      <p>🧠 AI Meaning: {response}</p>


      
    </div>
  );
}

export default App;

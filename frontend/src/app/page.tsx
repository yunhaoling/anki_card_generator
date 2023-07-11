'use client';

import { blob } from 'node:stream/consumers';
import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [responseText, setResponseText] = useState('');
  const [audioFile, setAudioFile] = useState('');
  const [audioBytes, setAudioBytes] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSendText = () => {
    // Send the text to the server and handle the response
    // Make an API request to the server, e.g., using fetch
    fetch('http:///127.0.0.1:5123/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ word: inputText }),
    })
      .then((response) => response.json())
      .then((data) => {
        setResponseText(data.translation);
        setAudioFile(data.audio);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const handlePlayAudio = () => {
    // Play the audio file
    // console.warn("I am here")
    // console.warn(audioFile)
    const audioData = atob(audioFile);
    var bytes = new Uint8Array(audioData.length);
    for (var i = 0; i < audioData.length; i++) {
        bytes[i] = audioData.charCodeAt(i);
    }
    console.warn(bytes)
    setAudioBytes(new Uint8Array(bytes))
    console.warn(audioBytes)
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    audioContext.decodeAudioData(bytes.buffer, (buffer) => {
      const source = audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContext.destination);
      source.start();
    });

  };

  const handleStoreAudio = () => {
    // Trigger audio file download
    // const link = document.createElement('a');
    // link.href = audioFile;
    // link.download = 'audio.wav';
    // link.click();
    if (audioBytes.buffer) {
        const blob = new Blob([audioBytes.buffer], { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
  
        const link = document.createElement('a');
        link.href = url;
        link.download = 'audio.wav';
        link.click();
      }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Create a FormData object and append the file to it
    const formData = new FormData();
    formData.append('file', selectedFile);

    // Make an HTTP POST request to the API endpoint
    fetch('http:///127.0.0.1:5123/csv_to_anki', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
  
        const link = document.createElement('a');
        link.href = url;
        link.download = 'somefile.apkg';
        link.click();
      })
      .catch((error) => {
        // Handle errors
        console.error(error);
      });
  };

  return (
    <div>
      <input type="text" value={inputText} onChange={handleInputChange} />
      <button onClick={handleSendText}>Send Text</button>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      <p>{responseText}</p>
      {audioFile && (
        <div>
          <button onClick={handlePlayAudio}>Play Audio</button>
          <button onClick={handleStoreAudio}>Store Audio</button>
        </div>
      )}
    </div>
  );
}

export default App;

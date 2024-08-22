import { useState } from 'react';
import axios from 'axios';

export default function Transcribe() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/transcribe', formData, {
        responseType: 'blob',  // This is important to handle the file as a blob
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${file.name.split('.')[0]}_transcription.txt`);  // Set download filename
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);  // Clean up the link element

    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Transcribe Video</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button type="submit" disabled={!file || loading}>
          {loading ? 'Transcribing...' : 'Upload and Transcribe'}
        </button>
      </form>
    </div>
  );
}

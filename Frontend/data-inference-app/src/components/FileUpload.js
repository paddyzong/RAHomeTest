import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ setFileUrl, resetFile, setMessage, setIsDataProcessed }) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setIsDataProcessed(false);
    setError('');
    resetFile();
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/core/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setFileUrl(response.data.file_url);
      setMessage('The file has been uploaded. Click process to infer types.');
    } catch (err) {
      console.log(err)
      setMessage('File upload failed.');
    }
  };

  return (
    <div>
      <input type="file" accept=".csv,.xlsx" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload File</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default FileUpload;

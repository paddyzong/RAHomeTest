import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ setFileUrl, resetFile }) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
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
      //const response = await axios.post('/core/process/');
      //console.log(response.data);
      setFileUrl(response.data.file_url);
    } catch (err) {
      console.log(err)
      setError('File upload failed.');
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

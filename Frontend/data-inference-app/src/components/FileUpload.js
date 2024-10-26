import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ setData }) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
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

      console.log(response.data);
      setData(response.data);
    } catch (err) {
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

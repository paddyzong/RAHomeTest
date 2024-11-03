import React, { useState } from 'react';
import axios from 'axios';
import StyledButton from './StyledButton';

const FileUpload = ({ setFileUrl, resetFile, setMessage, setError, setIsDataProcessed }) => {
  const [file, setFile] = useState(null);
  // const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setIsDataProcessed(false);
    setMessage(null);
    setError(null);
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
      setError(null);
    } catch (err) {
      console.log(err)
      setError('File upload failed.');
    }
  };

  return (
    <div className="flex flex-col items-center mt-4"> 
      <div className="flex items-center space-x-2">
        <input
          type="file"
          accept=".csv,.xlsx"
          className="text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onChange={handleFileChange} />
        <StyledButton onClick={handleUpload} >Upload File</StyledButton>
      </div>
    </div>
  );
};

export default FileUpload;

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
    <div className="flex flex-row items-center mt-4"> 
        <input
          type="file"
          accept=".csv,.xlsx"
          style={{marginLeft:'1em',marginTop:'1em'}}
          onChange={handleFileChange} />
        <StyledButton onClick={handleUpload} style={{ marginLeft: "auto", marginTop:'1em', marginRight:'1em'}}>Upload File</StyledButton>
    </div>
  );
};

export default FileUpload;

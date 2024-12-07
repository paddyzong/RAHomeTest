import React, { useState } from 'react';
import axios from 'axios';
import StyledButton from './StyledButton';
import { Upload } from 'tus-js-client'; 
import { useDataContext } from './DataContext';

const FileUpload = ({ onUploaded, resetFile, setMessage, setError, setIsDataProcessed }) => {
  const [file, setFile] = useState(null);
  const { clearData } = useDataContext();
  const MAX_FILE_SIZE = 100 * 1024 * 1024;
  // const [error, setError] = useState('');

  const handleFileChange = (e) => {
    clearData();
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

    // Check if the file size exceeds 100MB
    if (file.size > MAX_FILE_SIZE) {
      // Use Tus for large files
      uploadWithTus(file);
    } else {
      // Use regular upload for smaller files
      uploadWithTus(file);
      uploadWithAxios(file);
    }
  };

  // Upload function using Tus for large files
  const uploadWithAxios = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/core/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onUploaded(response.data.file_url, false);
      setMessage('The file has been uploaded. Click process to infer types.');
      setError(null);
    } catch (err) {
      setMessage(null);
      console.error(err);
      setError('File upload failed.');
    }
  };

  // Upload function using Tus for large files
  const uploadWithTus = (file) => {
    const upload = new Upload(file, {
      endpoint: 'http://localhost:8000/tus/files/',
      // endpoint: '/tus/files/', 
      metadata: {
        filename: file.name,
        filetype: file.type,
      },
      chunkSize: 512 * 1024 * 1024,
      onError: (error) => {
        console.error("Tus upload failed:", error);
        setMessage(null);
        setError('File upload failed.');
      },
      onProgress: (bytesUploaded, bytesTotal) => {
        const percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2);
        setMessage(`Upload Progress: ${percentage}%`);
      },
      onSuccess: () => {
        const url = upload.url;
        const id = url.split("/")[3]
        console.log("Upload finished:", id);
        onUploaded(id, true)
        setMessage('The file has been uploaded. Click process to infer types.');
        setError(null);
      },
    });
    // Check if there are any previous uploads to continue.
    upload.findPreviousUploads().then(function (previousUploads) {
      // Found previous uploads so we select the first one.
      if (previousUploads.length) {
        upload.resumeFromPreviousUpload(previousUploads[0])
      }

      // Start the upload
      upload.start()
    })
  };

  return (
    <div className="flex flex-row items-center mt-4">
      <input
        type="file"
        accept=".csv,.xlsx"
        style={{ marginLeft: '1em', marginTop: '1em' }}
        onChange={handleFileChange} />
      <StyledButton onClick={handleUpload} style={{ marginLeft: "auto", marginTop: '1em', marginRight: '1em' }}>Upload File</StyledButton>
    </div>
  );
};

export default FileUpload;

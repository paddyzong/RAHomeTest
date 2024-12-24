import React, { useState } from 'react';
import api from '../services/api';
import StyledButton from './StyledButton';
import { Upload } from 'tus-js-client';
import { useDataContext } from './DataContext';

const FileUpload = ({ onUploaded, resetFile, setMessage, setError, setIsDataProcessed }) => {
  const [file, setFile] = useState(null);
  const { clearData } = useDataContext();
  const MAX_FILE_SIZE = 100 * 1024 * 1024;
  const IS_AWS = process.env.REACT_APP_IS_AWS === "true";
  const apiBaseUrl = process.env.REACT_APP_API_BASE_URL; // Load from .env

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
    if (IS_AWS) {
      uploadWithS3(file);
    }
    else {
      uploadWithTus(file);
    }
  };

  const uploadWithAxios = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/core/upload/', formData, {
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

  const uploadWithS3 = async (file) => {
    try {
      // Step 1: Request presigned URL from the backend
      const response = await api.post("/core/get-presigned-url/", {
        fileName: file.name,
        fileType: file.type,
      });

      const { url } = response.data;

      // Step 2: Upload file directly to S3 using the presigned URL
      await api.put(url, file, {
        headers: {
          "Content-Type": file.type,
        },
      });

      setMessage("File uploaded successfully to AWS S3!");
      const fileKey = url.split('?')[0];
      onUploaded(fileKey, false);
    } catch (error) {
      console.error("Error uploading to S3:", error);
      setError("S3 upload failed. Please try again.");
    }
  };

  const endpoint = `${apiBaseUrl}/tus/files/`;
  // Upload function using Tus for large files
  const uploadWithTus = (file) => {
    const upload = new Upload(file, {
      endpoint: endpoint,
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
        const id = url.split("/").slice(-2)[0]
        console.log("Upload finished:", url);
        console.log("Upload finished:", id);
        onUploaded(id, true)
        setMessage('The file has been uploaded. Click process to infer types.');
        setError(null);
      },
    });
    // Check if there are any previous uploads to continue.
    upload.findPreviousUploads().then(function (previousUploads) {
      if (previousUploads.length) {
        upload.resumeFromPreviousUpload(previousUploads[0])
      }
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

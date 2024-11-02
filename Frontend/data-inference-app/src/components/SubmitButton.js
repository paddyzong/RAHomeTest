import React from 'react';
import axios from 'axios';

const SubmitButton = ({ data, types, fileUrl, setData, setTypes, setMessage, setTotalRecords, showTypeSelectors, onProcessComplete }) => {
  const handleSubmit = async () => {
    try {
      const response = await axios.post('/core/process/', { fileUrl, types, specifyTypesManually: showTypeSelectors, });
      if (response.data.total_records <= 0) {
        alert("No data available.");
        return;
      }
      setMessage("");
      onProcessComplete();
      setTotalRecords(response.data.total_records);
      alert('Data processed successfully!');
    } catch (err) {
      if (err.response) {
        // Server responded with a status other than 200 range
        const { status, data } = err.response;
        if (status === 400) {
          setMessage(data.error || 'Invalid input data.');
        } else if (status === 500) {
          setMessage('Server error: Please try again later.');
        } else {
          setMessage(`Unexpected error: ${status} - ${data.message || 'Please check your input or try again later.'}`);
        }
      } else if (err.request) {
        // Request was made but no response received
        setMessage('No response from server. Please check your internet connection or try again later.');
      } else {
        // Something else happened in setting up the request
        setMessage('Error: ' + err.message);
      }
    }
  };

  return <button onClick={handleSubmit}>Process</button>;
};

export default SubmitButton;

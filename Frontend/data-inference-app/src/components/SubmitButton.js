import React from 'react';
import axios from 'axios';
import StyledButton from './StyledButton';

const SubmitButton = ({ types, fileUrl, setMessage, setError, setTotalRecords, showTypeSelectors, onProcessComplete, setIsDataProcessed }) => {
  const handleSubmit = async () => {
    try {
      const response = await axios.post('/core/process/', { fileUrl, types, specifyTypesManually: showTypeSelectors, });
      if (response.data.total_records <= 0) {
        alert("No data available.");
        return;
      }
      setMessage(null);
      setError(null);
      setIsDataProcessed(true);
      onProcessComplete();
      setTotalRecords(response.data.total_records);
      alert('Data processed successfully!');
    } catch (err) {
      if (err.response) {
        // Server responded with a status other than 200 range
        const { status, data } = err.response;
        if (status === 400) {
          setError(data.error || 'Invalid input data.');
        } else if (status === 500) {
          setError('Server error: Please try again later.');
        } else {
          setError(`Unexpected error: ${status} - ${data.message || 'Please check your input or try again later.'}`);
        }
      } else if (err.request) {
        // Request was made but no response received
        setError('No response from server. Please check your internet connection or try again later.');
      } else {
        // Something else happened in setting up the request
        setError('Error: ' + err.message);
      }
    }
  };

  return <StyledButton onClick={handleSubmit}>Process</StyledButton>;
};

export default SubmitButton;

import React from 'react';
import api from '../services/api';
import StyledButton from './StyledButton';
import { useAppContext } from './AppContext';

const SubmitButton = ({ buttonText = 'Process', isCelery = false}) => {
  const { setIsCelery, types, fileUrl, isTusUpload, setMessage, setError, setTotalRecords, showTypeSelectors, onProcessComplete, setIsDataProcessed  } = useAppContext();
  const handleSubmit = async () => {
    try {
      if (fileUrl.endsWith(".xlsx") || fileUrl.endsWith(".xls")) {
        if(isCelery)
          {
            alert('Celery processes for excel files are not supported!');
            return
          }
      }
      const response = await api.post('/core/process/', { fileUrl, isTusUpload, isCelery, types, specifyTypesManually: showTypeSelectors, });
      if (response.data.total_records <= 0) {
        alert("No data available.");
        return;
      }
      setMessage(null);
      setError(null);
      setIsCelery(isCelery);
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

  return <StyledButton style={{marginTop:'1em'}} onClick={handleSubmit}>{buttonText}</StyledButton>;
};

export default SubmitButton;

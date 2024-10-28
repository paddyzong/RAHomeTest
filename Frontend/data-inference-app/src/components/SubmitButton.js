import React from 'react';
import axios from 'axios';

const SubmitButton = ({ data, types, fileUrl, setData }) => {
  const handleSubmit = async () => {
    try {
      const response = await axios.post('/core/process/', { fileUrl, types });
      //console.log(response);
      const parsedArray = JSON.parse(response.data);
      console.log(parsedArray);
      setData(parsedArray)
      alert('Data processed successfully!');
    } catch (err) {
      alert('Failed to process data.');
    }
  };

  return <button onClick={handleSubmit}>Submit Processed Data</button>;
};

export default SubmitButton;

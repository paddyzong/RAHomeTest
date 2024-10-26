import React from 'react';
import axios from 'axios';

const SubmitButton = ({ data, types }) => {
  const handleSubmit = async () => {
    try {
      const response = await axios.post('/process/', { data, types });
      alert('Data processed successfully!');
    } catch (err) {
      alert('Failed to process data.');
    }
  };

  return <button onClick={handleSubmit}>Submit Processed Data</button>;
};

export default SubmitButton;

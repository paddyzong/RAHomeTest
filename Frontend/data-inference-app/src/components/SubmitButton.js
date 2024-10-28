import React from 'react';
import axios from 'axios';

const SubmitButton = ({ data, types, fileUrl, setData, setTypes }) => {
  const handleSubmit = async () => {
    try {
      const response = await axios.post('/core/process/', { fileUrl, types });
      //console.log(response);
      const jsonData = response.data.replace(/NaN/g, "null");
      const parsedArray = JSON.parse(jsonData);
      console.log(parsedArray.data);
      setData(parsedArray.data)
      setTypes(parsedArray.types)
      alert('Data processed successfully!');
    } catch (err) {
      console.log(err)
      alert('Failed to process data.');
    }
  };

  return <button onClick={handleSubmit}>Submit Processed Data</button>;
};

export default SubmitButton;

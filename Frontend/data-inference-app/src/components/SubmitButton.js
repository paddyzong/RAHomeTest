import React from 'react';
import axios from 'axios';

const SubmitButton = ({ data, types, fileUrl, setData, setTypes, showTypeSelectors }) => {
  const handleSubmit = async () => {
    try {
      const response = await axios.post('/core/process/', { fileUrl, types, specifyTypesManually: showTypeSelectors, });
      console.log(response);
      //const jsonData = response.data.replace(/NaN/g, "null");
      //const parsedArray = JSON.parse(jsonData);
      //console.log(parsedArray.data);
      setData(response.data.data)
      setTypes(response.data.types)
      alert('Data processed successfully!');
    } catch (err) {
      console.log(err)
      alert('Failed to process data.');
    }
  };

  return <button onClick={handleSubmit}>Submit Processed Data</button>;
};

export default SubmitButton;

import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';

const App = () => {
  const [data, setData] = useState(null);
  const [types, setTypes] = useState(null);
  const [fileUrl, setFileUrl] = useState("");
  console.log(fileUrl)
  const handleFileUrlChange = (newUrl) => {
    setFileUrl(newUrl);
  };
  const handleSetData = (data) => {
    console.log(111);
    console.log(data[0]);
    console.log(Object.keys(data[0]));
    setData(data);       // Raw data
    setTypes(Object.keys(data[0]));     // Inferred types
  };

  return (
    <div>
      <h1>Data Type Inference App</h1>
      <FileUpload setFileUrl={handleFileUrlChange} />
      {fileUrl && (
        <>
          <DataTable data={data} types={types} setTypes={setTypes} />
          <SubmitButton data={data} types={types} fileUrl={fileUrl} setData={handleSetData} />
        </>
      )}
    </div>
  );
};

export default App;

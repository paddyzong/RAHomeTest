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
    console.log("setdata");
    console.log(data);
    setData(data);       // Raw data
  };
  const handleSetTypes = (types) => {
    setTypes(types);       // Raw data
  };

  return (
    <div>
      <FileUpload setFileUrl={handleFileUrlChange} />
      {fileUrl && (
        <>
          <DataTable data={data} types={types} setTypes={setTypes} />
          <SubmitButton data={data} types={types} fileUrl={fileUrl} setData={handleSetData} setTypes={handleSetTypes}/>
        </>
      )}
    </div>
  );
};

export default App;

import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';

const App = () => {
  const [data, setData] = useState(null);
  const [types, setTypes] = useState(null);
  const [fileUrl, setFileUrl] = useState("");
  const [showTypeSelectors, setShowTypeSelectors] = useState(false);
  //console.log(fileUrl)
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
  const toggleTypeSelectors = () => {
    setShowTypeSelectors((prev) => !prev);
  };
  const handleFileReset = () => {
    setData(null);
    setFileUrl(null);
    setTypes(null);
    setShowTypeSelectors(false);
  };
  return (
    <div>
      <FileUpload setFileUrl={handleFileUrlChange} resetFile={handleFileReset}/>
      {fileUrl && (
        <>
          <DataTable data={data} types={types} setTypes={setTypes} showTypeSelectors={showTypeSelectors} toggleTypeSelectors={toggleTypeSelectors}/>
          <SubmitButton data={data} types={types} fileUrl={fileUrl} setData={handleSetData} setTypes={handleSetTypes} showTypeSelectors={showTypeSelectors} />
        </>
      )}
    </div>
  );
};

export default App;

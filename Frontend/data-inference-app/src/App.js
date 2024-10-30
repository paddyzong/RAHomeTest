import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';

const App = () => {
  const [data, setData] = useState(null);
  const [types, setTypes] = useState(null);
  const [fileUrl, setFileUrl] = useState("");
  const [message, setMessage] = useState("");
  const [showTypeSelectors, setShowTypeSelectors] = useState(false);

  const handleFileUrlChange = (newUrl) => {
    setFileUrl(newUrl);
  };

  const handleSetData = (newData) => {
    console.log("Data updated:", newData);
    setData(newData);
  };

  const handleSetTypes = (newTypes) => {
    setTypes(newTypes);
  };

  const toggleTypeSelectors = () => {
    setShowTypeSelectors((prev) => !prev);
  };

  const handleFileReset = () => {
    setData(null);
    setFileUrl("");
    setTypes(null);
    setShowTypeSelectors(false);
  };

  return (
    <div>
      <FileUpload setFileUrl={handleFileUrlChange} setMessage={setMessage} resetFile={handleFileReset}/>
      {fileUrl && (
        <>
          <DataTable 
            data={data} 
            types={types} 
            message={message} 
            setTypes={setTypes} 
            showTypeSelectors={showTypeSelectors} 
            toggleTypeSelectors={toggleTypeSelectors}
          />
          <SubmitButton 
            data={data} 
            types={types} 
            fileUrl={fileUrl} 
            setData={handleSetData} 
            setTypes={handleSetTypes} 
            setMessage={setMessage} 
            showTypeSelectors={showTypeSelectors} 
          />
        </>
      )}
    </div>
  );
};

export default App;

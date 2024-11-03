import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';

const App = () => {
  const [data, setData] = useState(null);
  const [types, setTypes] = useState(null);
  const [fileUrl, setFileUrl] = useState("");
  const [message, setMessage] = useState(null);
  const [isDataProcessed, setIsDataProcessed] = useState(false);
  const [error, setError] = useState("");
  const [totalRecords, setTotalRecords] = useState(0); 
  const [refreshTrigger, setRefreshTrigger] = useState(0);
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

  const isNotBlank = (str) => str && str.trim().length > 0;
  
  return (
    <div>
      <FileUpload 
        setFileUrl={handleFileUrlChange} 
        setMessage={setMessage} 
        setError={setError}
        resetFile={handleFileReset}
        setIsDataProcessed={setIsDataProcessed}
        />
      {message && (<p>{message}</p>)}
      {error && (<p style={{ color: 'red' }}>{error}</p>)} 
      {fileUrl && (
        <>
          {isDataProcessed && (<DataTable 
            totalRecords={totalRecords}
            setError={setError} 
            handleSetTypes={handleSetTypes} 
            showTypeSelectors={showTypeSelectors} 
            refreshTrigger={refreshTrigger}
            //clearDataTrigger={clearDataTrigger}
            toggleTypeSelectors={toggleTypeSelectors}
          />)}
          <SubmitButton 
            data={data} 
            types={types} 
            fileUrl={fileUrl} 
            setData={handleSetData} 
            setMessage={setMessage} 
            setError={setError}
            setTotalRecords={setTotalRecords}
            showTypeSelectors={showTypeSelectors} 
            setIsDataProcessed={setIsDataProcessed}
            onProcessComplete={() => setRefreshTrigger(prev => prev + 1)}
          />
        </>
      )}
    </div>
  );
};

export default App;

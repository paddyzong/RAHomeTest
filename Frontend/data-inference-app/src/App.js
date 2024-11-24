import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';
import './style.css';

const App = () => {
  const [data, setData] = useState(null);
  const [types, setTypes] = useState(null);
  const [fileUrl, setFileUrl] = useState("");
  const [isTusUpload, setIsTusUpload] = useState(false);
  const [isCelery, setIsCelery] = useState(false);
  const [message, setMessage] = useState(null);
  const [isDataProcessed, setIsDataProcessed] = useState(false);
  const [error, setError] = useState("");
  const [totalRecords, setTotalRecords] = useState(0);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [showTypeSelectors, setShowTypeSelectors] = useState(false);

  const outerDivStyle = {  
    width:'auto',
    overflowY: 'auto',   
    overflowX: 'auto',
  };
  const innerDivStyle = { 
    width:'auto',
    //display: 'inline-block',      
    //width: 'fit-content',
  };

  const onUploaded = (fileUrl, isTusUpload) => {
    setFileUrl(fileUrl);
    setIsTusUpload(isTusUpload);
  };

  const handleSetData = (newData) => {
    console.log("Data updated:", newData);
    setData(newData);
  };

  const handleSetTypes = (newTypes) => {
    setTypes(newTypes);
  };
  const handleTypeChange = (idx, newType) => {
    const updatedTypes = [...types];
    updatedTypes[idx] = newType;
    setTypes(updatedTypes);
    handleSetTypes(updatedTypes);
  };

  const toggleTypeSelectors = () => {
    setShowTypeSelectors((prev) => !prev);
  };

  const handleFileReset = () => {
    setData(null);
    setFileUrl("");
    setTypes(null);
    setShowTypeSelectors(false);
    setIsCelery(false);
    setError(""); // Clear error when resetting
  };

  const isNotBlank = (str) => str && str.trim().length > 0;

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6"style={outerDivStyle}>
      <div className="bg-white shadow-lg rounded-lg p-6 w-full" style={innerDivStyle}>
        <FileUpload
          onUploaded={onUploaded}
          setMessage={setMessage}
          resetFile={handleFileReset}
          setIsDataProcessed={setIsDataProcessed}
          setError={setError}
        />

        {message && (<p className="text-center text-green-500 my-2">{message}</p>)}
        {error && (<p className="text-center text-red-500 my-2">{error}</p>)}

        {fileUrl && (
          <div className="mt-4">
            {isDataProcessed && (
              <DataTable
                types={types}
                fileUrl={fileUrl}
                isCelery={isCelery}
                isTusUpload={isTusUpload}
                totalRecords={totalRecords}
                setError={setError}
                setMessage={setMessage}
                setTypes={setTypes}
                handleTypeChange={handleTypeChange}
                showTypeSelectors={showTypeSelectors}
                refreshTrigger={refreshTrigger}
                toggleTypeSelectors={toggleTypeSelectors}
              />
            )}

            <SubmitButton
              data={data}
              types={types}
              fileUrl={fileUrl}
              isTusUpload={isTusUpload}
              setIsCelery={setIsCelery}
              setData={handleSetData}
              setMessage={setMessage}
              setTotalRecords={setTotalRecords}
              showTypeSelectors={showTypeSelectors}
              setIsDataProcessed={setIsDataProcessed}
              onProcessComplete={() => setRefreshTrigger(prev => prev + 1)}
              setError={setError}
            />
            <SubmitButton
              buttonText = 'Use Celery to process'
              isCelery = {true}
              data={data}
              types={types}
              fileUrl={fileUrl}
              isTusUpload={isTusUpload}
              setIsCelery={setIsCelery}
              setData={handleSetData}
              setMessage={setMessage}
              setTotalRecords={setTotalRecords}
              showTypeSelectors={showTypeSelectors}
              setIsDataProcessed={setIsDataProcessed}
              onProcessComplete={() => setRefreshTrigger(prev => prev + 1)}
              setError={setError}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;

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
  const [message, setMessage] = useState(null);
  const [isDataProcessed, setIsDataProcessed] = useState(false);
  const [error, setError] = useState("");
  const [totalRecords, setTotalRecords] = useState(0);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [showTypeSelectors, setShowTypeSelectors] = useState(false);

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

  const toggleTypeSelectors = () => {
    setShowTypeSelectors((prev) => !prev);
  };

  const handleFileReset = () => {
    setData(null);
    setFileUrl("");
    setTypes(null);
    setShowTypeSelectors(false);
    setError(""); // Clear error when resetting
  };

  const isNotBlank = (str) => str && str.trim().length > 0;

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-2xl">
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
                totalRecords={totalRecords}
                setError={setError}
                setMessage={setMessage}
                handleSetTypes={handleSetTypes}
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

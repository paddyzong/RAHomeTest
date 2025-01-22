import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';
import { useAppContext } from './components/AppContext';
import './style.css';

const App = () => {
  const { fileUrl, message, error, isDataProcessed } = useAppContext();
  const outerDivStyle = {
    width: 'auto',
    overflowY: 'auto',
    overflowX: 'auto',
  };
  const innerDivStyle = {
    width: 'auto',
  };

  const isNotBlank = (str) => str && str.trim().length > 0;

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6" style={outerDivStyle}>
      <div className="bg-white shadow-lg rounded-lg p-6 w-full" style={innerDivStyle}>
          <FileUpload/>
          {message && (<p className="text-center text-green-500 my-2">{message}</p>)}
          {error && (<p className="text-center text-red-500 my-2">{error}</p>)}

          {fileUrl && (
            <div className="mt-4">
              {isDataProcessed && (
                <DataTable/>
              )}
              <div>
                <SubmitButton/>
                <SubmitButton buttonText='Use Celery to process' isCelery={true} />
              </div>
            </div>
          )}
      </div>
    </div>
  );
};

export default App;

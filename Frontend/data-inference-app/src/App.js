import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import SubmitButton from './components/SubmitButton';

const App = () => {
  const [data, setData] = useState(null);
  const [types, setTypes] = useState(null);

  const handleSetData = (responseData) => {
    setData(responseData.data);       // Raw data
    setTypes(responseData.types);     // Inferred types
  };

  return (
    <div>
      <h1>Data Type Inference App</h1>
      <FileUpload setData={handleSetData} />
      {data && types && (
        <>
          <DataTable data={data} types={types} setTypes={setTypes} />
          <SubmitButton data={data} types={types} />
        </>
      )}
    </div>
  );
};

export default App;

import React, { createContext, useState, useContext } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [data, setData] = useState([]);
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

  const clearData = () => {
    setData([]);
  };
  const onUploaded = (fileUrl, isTusUpload) => {
    setFileUrl(fileUrl);
    setIsTusUpload(isTusUpload);
  };

  const handleSetData = (newData) => {
    console.log("Data updated:", newData);
    setData(newData);
  };

  const handleTypeChange = (idx, newType) => {
    setTypes((prevTypes) => {
      const updatedTypes = [...prevTypes];
      updatedTypes[idx] = newType;
      return updatedTypes;
    });
  };

  const toggleTypeSelectors = () => {
    setShowTypeSelectors((prev) => !prev);
  };

  const resetFile = () => {
    setData(null);
    setFileUrl("");
    setTypes(null);
    setShowTypeSelectors(false);
    setIsCelery(false);
    setError(""); // Clear error when resetting
  };

  return (
    <AppContext.Provider
      value={{
        data,
        types,
        fileUrl,
        isTusUpload,
        isCelery,
        message,
        isDataProcessed,
        error,
        totalRecords,
        refreshTrigger,
        onUploaded,
        handleSetData,
        handleTypeChange,
        toggleTypeSelectors,
        resetFile,
        setData,
        setTypes,
        setRefreshTrigger,
        clearData,
        setIsCelery,
        setMessage,
        setError,
        setTotalRecords,
        showTypeSelectors,
        onProcessComplete: () => setRefreshTrigger(prev => prev + 1),
        setIsDataProcessed
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);

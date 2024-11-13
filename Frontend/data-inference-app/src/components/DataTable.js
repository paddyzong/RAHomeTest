import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StyledButton from './StyledButton';

const DataTable = ({ setError, setMessage, handleSetTypes, showTypeSelectors, toggleTypeSelectors, refreshTrigger }) => {
  const [data, setData] = useState([]); // Data from the server
  const [types, setTypes] = useState([]);
  const [currentPage, setCurrentPage] = useState(1); // Track current page
  const [totalPages, setTotalPages] = useState(1); // Total pages from server response
  const [loading, setLoading] = useState(false); // Loading state

  const pDivStyle = {       // equivalent to "overflow-hidden"
    position: 'relative',        // equivalent to "relative"
    overflow: 'hidden',          // equivalent to "overflow-hidden"
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)', // equivalent to "shadow-md" (approximate)
    borderRadius: '0.5rem',  
  };
  
  const talbeStyle = {         // equivalent to "overflow-hidden"
    position: 'relative',        // equivalent to "relative"
    overflow: 'hidden',          // equivalent to "overflow-hidden"
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)', // equivalent to "shadow-md" (approximate)
    borderRadius: '0.5rem',  
    marginTop: '1em',
    marginLeft:'1em',
    width:'95%'
  };

  const headerStyle = {
    paddingTop: '0.25rem',     // equivalent to "py-1" (padding-top)
    paddingBottom: '0.25rem',  // equivalent to "py-1" (padding-bottom)
    padding: '1rem',           // equivalent to "p-4" (general padding)
    border: '1px solid #ccc',  // equivalent to "border" (approximate)
    textAlign: 'center',       // equivalent to "text-center"
  };

  const tBodyStyle = {
    backgroundColor: '#FFFFFF', // equivalent to "bg-white" or "bg-[#FFFFFF]"
    color: '#6b7280',           // equivalent to "text-gray-500" or "text-[#6b7280]"
  };

  const trStyle = {
    paddingTop: '0.5rem',     // equivalent to "py-5" (padding-top)
    paddingBottom: '0.5rem',  // equivalent to "py-5" (padding-bottom)
  };
  const tdStyle = {
    paddingTop: '0.5rem',       // Reduce padding to make cells smaller
    paddingBottom: '0.5rem',    // Reduce padding to make cells smaller
    paddingLeft: '0.5rem',      // Reduce padding to make cells smaller
    paddingRight: '0.5rem',     // Reduce padding to make cells smaller
    border: '1px solid #ccc',   // equivalent to "border" (approximate)
    textAlign: 'center',        // equivalent to "text-center"
  };
  //console.log("refreshTrigger:"+refreshTrigger);
  //console.log("current page:" + currentPage);
  const handleTypeChange = (idx, newType) => {
    const updatedTypes = [...types];
    updatedTypes[idx] = newType;
    setTypes(updatedTypes);
    handleSetTypes(updatedTypes);
  };

  // Fetch data from the server for the current page
  const fetchData = async (page) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const response = await axios.post('/core/view/', { page, });
      //console.log(response);
      setData(response.data.records); // Update data with records from response
      setTypes(response.data.types);
      setTotalPages(response.data.total_pages); // Set total pages from response
    } catch (error) {
      setMessage(null);
      setError('Error fetching data.');
    } finally {
      setLoading(false);
    }
  };

  // useEffect(() => {
  //   if (currentPage !== 1)
  //     setCurrentPage(1);
  //   else
  //     fetchData(currentPage);
  // }, [refreshTrigger, currentPage]);

  useEffect(() => {
    if (currentPage !== 1)
      setCurrentPage(1);
    // else
    //   fetchData(currentPage);
  }, [refreshTrigger]);

  useEffect(() => {
    fetchData(currentPage);
  }, [currentPage]);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  if (data?.length > 0)
    return (
      <div style={pDivStyle}>
        <StyledButton style={{marginLeft:'1em'}}onClick={toggleTypeSelectors}>
          {showTypeSelectors ? 'Let System Infer Types' : 'Specify Types Manually'}
        </StyledButton>
        {loading ? (
          <p>Loading data...</p>
        ) : <table style={talbeStyle}> 
          <thead style={{backgroundColor: '#6b7280', color: '#e5e7eb'}}>
            <tr>
              {Object.keys(data[0]).map((column, idx) => (
                <th style={headerStyle}
                  key={column}>
                  {column}
                  <br />
                  {showTypeSelectors ? (
                    <select style={{color:'#374151'}}
                      value={types[idx] || 'Text'}
                      onChange={(e) => handleTypeChange(idx, e.target.value)}
                    >
                      <option value="Text">Text</option>
                      <option value="Integer">Integer</option>
                      <option value="Decimal">Decimal</option>
                      <option value="Boolean">Boolean</option>
                      <option value="Date">Date</option>
                      <option value="Duration">Duration</option>
                      <option value="Category">Category</option>
                    </select>
                  ) : (
                    <span>{types[idx] || 'Text'}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody style={tBodyStyle}>
            {data.map((row, rowIndex) => (
              <tr style={trStyle}
                key={rowIndex}>
                {Object.values(row).map((cell, cellIndex) => (
                  <td style={tdStyle}
                    key={cellIndex}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>}
        {/* Pagination Controls */}
        <div style={{marginBottom:'1em'}} className="flex items-center justify-center space-x-4 mt-4">
          <button
            onClick={handlePrevPage}
            disabled={currentPage === 1 || loading}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition duration-200 ease-in-out disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-gray-700 font-medium">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages || loading}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition duration-200 ease-in-out disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    );
};

export default DataTable;

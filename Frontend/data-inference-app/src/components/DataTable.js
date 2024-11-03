import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StyledButton from './StyledButton';

const DataTable = ({ setError, handleSetTypes, showTypeSelectors, toggleTypeSelectors, refreshTrigger, clearDataTrigger }) => {
  const [data, setData] = useState([]); // Data from the server
  const [types, setTypes] = useState([]);
  const [currentPage, setCurrentPage] = useState(1); // Track current page
  const [totalPages, setTotalPages] = useState(1); // Total pages from server response
  const [loading, setLoading] = useState(false); // Loading state

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
    try {
      const response = await axios.post('/core/view/', { page, });
      //console.log(response);
      setData(response.data.records); // Update data with records from response
      setTypes(response.data.types);
      setTotalPages(response.data.total_pages); // Set total pages from response
    } catch (error) {
      setError('Error fetching data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentPage !== 1)
      setCurrentPage(1);
    else
      fetchData(currentPage);
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
      <div>
        <StyledButton onClick={toggleTypeSelectors}>
          {showTypeSelectors ? 'Let System Infer Types' : 'Specify Types Manually'}
        </StyledButton>
        {loading ? (
          <p>Loading data...</p>
        ) : <table>
          <thead>
            <tr>
              {Object.keys(data[0]).map((column, idx) => (
                <th key={column}>
                  {column}
                  <br />
                  {showTypeSelectors ? (
                    <select
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
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {Object.values(row).map((cell, cellIndex) => (
                  <td key={cellIndex}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>}
        {/* Pagination Controls */}
        <div className="flex items-center justify-center space-x-4 mt-4">
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

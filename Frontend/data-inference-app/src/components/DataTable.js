import React from 'react';

const DataTable = ({ data, types, setTypes }) => {
  if (!data || !types) {
    return <p>No data available. Please upload a file.</p>;
  }
  const columns = Object.keys(data[0]);
  const handleTypeChange = (column, newType) => {
    const updatedTypes = { ...types, [column]: newType };
    setTypes(updatedTypes);
  };

  return (
    <div>
      <table>
        <thead>
          <tr>
            {Object.keys(columns).map((column) => (
              <th key={column}>
                {column} <br />
                <select
                  value={types[column]}
                  onChange={(e) => handleTypeChange(column, e.target.value)}
                >
                  <option value="object">Text</option>
                  <option value="int">Integer</option>
                  <option value="float">Float</option>
                  <option value="datetime64">Date</option>
                  <option value="bool">Boolean</option>
                  <option value="category">Category</option>
                </select>
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
      </table>
    </div>
  );
};

export default DataTable;

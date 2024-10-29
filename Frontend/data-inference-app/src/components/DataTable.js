import React, { useState } from 'react';

const DataTable = ({ data, types, setTypes, showTypeSelectors, toggleTypeSelectors }) => {
  //const [showTypeSelectors, setShowTypeSelectors] = useState(false);

  if (!data || !types) {
    return <p>The file has been uploaded. Click process to infer types.</p>;
  }

  const handleTypeChange = (idx, newType) => {
    const updatedTypes = [...types];
    updatedTypes[idx] = newType;
    console.log(idx)
    console.log(newType)
    setTypes(updatedTypes);
  };

  // const handleToggle = () => {
  //   setShowTypeSelectors(!showTypeSelectors);
  // };

  return (
    <div>
      <button onClick={toggleTypeSelectors}>
        {showTypeSelectors ? 'Let System Infer Types' : 'Specify Types Manually'}
      </button>
      <table>
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
      </table>
    </div>
  );
};

export default DataTable;

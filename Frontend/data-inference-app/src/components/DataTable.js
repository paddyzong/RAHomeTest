import React from 'react';

const DataTable = ({ data, types, setTypes }) => {
  if (!data || !types) {
    return <p>The file has been uploaded. Click process to infer types.</p>;
  }
  const handleTypeChange = (column, newType) => {
    const updatedTypes = { ...types, [column]: newType };
    setTypes(updatedTypes);
  };
  console.log(types);
  return (
    <div>
      <table>
        <thead>
          <tr>
            {Object.keys(data[0]).map((column,idx) => (
              <th key={column}>
                {column} <br />
                <select
                  value={types[idx]}
                  onChange={(e) => handleTypeChange(column, e.target.value)}
                >
                  <option value="Text">Text</option>
                  <option value="Integer">Integer</option>
                  <option value="Decimal">Decimal</option>
                  <option value="Boolean">Boolean</option>
                  <option value="Date">Date</option>
                  <option value="Duration">Duration</option>
                  <option value="Category">Category</option>
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

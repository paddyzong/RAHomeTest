// /mnt/data/StyledButton.js

import React from 'react';

function StyledButton({ children, onClick, type = "button" }) {
  return (
    <button
      type={type}
      onClick={onClick}
      className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition duration-200 ease-in-out"
    >
      {children}
    </button>
  );
}

export default StyledButton;

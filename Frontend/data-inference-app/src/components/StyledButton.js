// /mnt/data/StyledButton.js

import React, { useState } from 'react';

function StyledButton({ children, onClick, type = "button", className = "", style = {}}) {
  const [isHovered, setIsHovered] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

  const buttonStyle = {
    backgroundColor: '#3B82F6',       // equivalent to "bg-blue-500"
    color: '#FFFFFF',                 // equivalent to "text-white"
    fontWeight: 'bold',               // equivalent to "font-bold"
    paddingTop: '0.5rem',             // equivalent to "py-2"
    paddingBottom: '0.5rem',          // equivalent to "py-2"
    paddingLeft: '1rem',              // equivalent to "px-4"
    paddingRight: '1rem',             // equivalent to "px-4"
    borderRadius: '0.5rem',           // equivalent to "rounded-lg"
    outline: 'none',                  // equivalent to "focus:outline-none"
    transition: 'background-color 200ms ease-in-out, box-shadow 200ms ease-in-out', // equivalent to "transition duration-200 ease-in-out"
    margin: '1em'
  };

  const buttonHoverStyle = {
    backgroundColor: '#2563EB',       // equivalent to "hover:bg-blue-600"
  };
  
  const buttonFocusStyle = {
    boxShadow: '0 0 0 3px rgba(59, 130, 246, 0.5)',  // equivalent to "focus:shadow-outline"
  };
  return (
    <button
      onClick={onClick}
      style={{
        ...buttonStyle,
        ...(isHovered ? buttonHoverStyle : {}),
        ...(isFocused ? buttonFocusStyle : {}),
        ...style
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
    >
      {children}
    </button>
  );
}

export default StyledButton;

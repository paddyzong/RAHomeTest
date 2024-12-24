

import React, { useState } from 'react';

function StyledButton({ children, onClick, type = "button", className = "", style = {}}) {
  const [isHovered, setIsHovered] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

  const buttonStyle = {
    backgroundColor: '#3B82F6',       
    color: '#FFFFFF',                 
    fontWeight: 'bold',               
    paddingTop: '0.5rem',             
    paddingBottom: '0.5rem',          
    paddingLeft: '1rem',              
    paddingRight: '1rem',             
    borderRadius: '0.5rem',           
    outline: 'none',                  
    transition: 'background-color 200ms ease-in-out, box-shadow 200ms ease-in-out', 
    margin: '1em'
  };

  const buttonHoverStyle = {
    backgroundColor: '#2563EB',       
  };
  
  const buttonFocusStyle = {
    boxShadow: '0 0 0 3px rgba(59, 130, 246, 0.5)',  
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

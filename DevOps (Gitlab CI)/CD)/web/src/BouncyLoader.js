import React from 'react';
import { bouncy } from 'ldrs';

// Register the bouncy loader
bouncy.register();

const BouncyLoader = ({ 
  size = "45", 
  speed = "1.75", 
  color = "#667eea",
  className = ""
}) => {
  return (
    <div className={`bouncy-loader-container ${className}`}>
      <l-bouncy
        size={size}
        speed={speed}
        color={color}
      ></l-bouncy>
    </div>
  );
};

export default BouncyLoader;
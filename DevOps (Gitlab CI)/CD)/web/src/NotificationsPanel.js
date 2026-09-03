import React, { useState } from 'react';

const NotificationsPanel = () => {
  const [showPanel, setShowPanel] = useState(false);

  return (
    <div style={{ 
      position: 'fixed', 
      top: '20px', 
      right: '20px', 
      zIndex: 9999 
    }}>
      <button
        onClick={() => setShowPanel(!showPanel)}
        style={{
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '50%',
          width: '60px',
          height: '60px',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
        }}
        title="Panel de Notificaciones"
      >
        🔔
      </button>
      
      {showPanel && (
        <div style={{
          position: 'absolute',
          top: '70px',
          right: '0',
          width: '300px',
          backgroundColor: 'white',
          border: '2px solid #ddd',
          borderRadius: '10px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          padding: '20px',
          color: '#333'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#4CAF50' }}>
            🔔 Notificaciones
          </h3>
          <p>Panel de notificaciones funcionando!</p>
          <button
            onClick={() => alert('¡Funciona!')}
            style={{
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              padding: '10px 15px',
              cursor: 'pointer'
            }}
          >
            Probar
          </button>
        </div>
      )}
    </div>
  );
};

export default NotificationsPanel;
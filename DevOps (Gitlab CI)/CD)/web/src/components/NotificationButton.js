import React, { useState } from 'react';

const NotificationButton = () => {
  const [showPanel, setShowPanel] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const buttonStyle = {
    position: 'fixed',
    top: '20px',
    right: '20px',
    width: '60px',
    height: '60px',
    borderRadius: '50%',
    backgroundColor: '#007bff',
    border: 'none',
    color: 'white',
    fontSize: '24px',
    cursor: 'pointer',
    boxShadow: '0 4px 12px rgba(0,123,255,0.3)',
    zIndex: 1000,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.3s ease'
  };

  const panelStyle = {
    position: 'fixed',
    top: '90px',
    right: '20px',
    width: '320px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 8px 32px rgba(0,0,0,0.15)',
    zIndex: 999,
    display: showPanel ? 'block' : 'none',
    border: '1px solid #e0e0e0'
  };

  const headerStyle = {
    padding: '16px 20px',
    borderBottom: '1px solid #e0e0e0',
    backgroundColor: '#f8f9fa',
    borderRadius: '12px 12px 0 0',
    fontWeight: 'bold',
    color: '#333'
  };

  const contentStyle = {
    padding: '16px 20px',
    maxHeight: '300px',
    overflowY: 'auto'
  };

  const testNotifications = async () => {
    setLoading(true);
    try {
      const response = await fetch('/notifications/health');
      const data = await response.json();
      alert('🎉 Notificaciones API funcionando: ' + JSON.stringify(data));
    } catch (error) {
      alert('❌ Error conectando con notificaciones: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <>
      <button 
        style={buttonStyle}
        onClick={() => setShowPanel(!showPanel)}
        title="Notificaciones"
      >
        🔔
      </button>
      
      <div style={panelStyle}>
        <div style={headerStyle}>
          🔔 Notificaciones
        </div>
        <div style={contentStyle}>
          <p style={{margin: '0 0 16px 0', color: '#666'}}>
            Sistema de notificaciones activado
          </p>
          
          <button
            onClick={testNotifications}
            disabled={loading}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              marginBottom: '8px',
              fontSize: '14px'
            }}
          >
            {loading ? '⏳ Probando...' : '🧪 Probar API'}
          </button>
          
          <button
            onClick={() => setShowPanel(false)}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            ❌ Cerrar
          </button>
        </div>
      </div>
    </>
  );
};

export default NotificationButton;
import React, { useState, useEffect } from 'react';
import './DockerDiagram.css';

const DockerDiagram = () => {
  const [containerStats, setContainerStats] = useState({
    total: 5,
    running: 5,
    healthy: 5,
    unhealthy: 0
  });

  const [services] = useState([
    {
      id: 'nginx',
      name: 'Proxy Nginx',
      container: 'todos-nginx',
      image: 'nginx:1.29-alpine',
      port: '80',
      status: 'healthy',
      description: 'Proxy reverso y balanceador de carga',
      category: 'proxy',
      connections: ['web', 'api', 'notifications']
    },
    {
      id: 'web',
      name: 'Frontend Web',
      container: 'todos-web',
      image: 'React 18.2 + Nginx 1.25',
      port: '3000',
      status: 'healthy',
      description: 'Aplicación frontend React',
      category: 'frontend',
      connections: []
    },
    {
      id: 'api',
      name: 'API Backend',
      container: 'todos-api',
      image: 'Python 3.11-alpine + Flask 3.1',
      port: '5000',
      status: 'healthy',
      description: 'API REST para operaciones de tareas',
      category: 'backend',
      connections: ['db']
    },
    {
      id: 'notifications',
      name: 'Notificaciones',
      container: 'todos-notifications',
      image: 'Python 3.11-slim + FastAPI 0.118',
      port: '8001',
      status: 'healthy',
      description: 'Servicio de notificaciones por correo',
      category: 'service',
      connections: ['db']
    },
    {
      id: 'db',
      name: 'Base de Datos MySQL',
      container: 'todos-db',
      image: 'MySQL 9.4',
      port: '3306',
      status: 'healthy',
      description: 'Almacenamiento persistente de datos',
      category: 'database',
      connections: []
    }
  ]);

  const features = [
    {
      icon: 'BUILD',
      title: 'Construcciones Multi-Etapa',
      description: 'Imágenes de contenedor optimizadas con etapas de construcción y producción separadas'
    },
    {
      icon: 'SECURITY',
      title: 'Usuarios No-Root',
      description: 'Todos los contenedores se ejecutan con usuarios de bajos privilegios por seguridad'
    },
    {
      icon: 'SECRETS',
      title: 'Docker Secrets',
      description: 'Gestión segura de credenciales sin exposición de código'
    },
    {
      icon: 'HEALTH',
      title: 'Health Checks',
      description: 'Monitoreo automático del estado de todos los servicios'
    },
    {
      icon: 'NETWORK',
      title: 'Docker Networks',
      description: 'Comunicación aislada entre contenedores'
    },
    {
      icon: 'STORAGE',
      title: 'Persistent Volumes',
      description: 'Persistencia de datos para la base de datos MySQL'
    }
  ];

  // Simulamos verificación de estado de contenedores
  useEffect(() => {
    const checkContainerHealth = async () => {
      try {
        // En una implementación real, esto consultaría la API de Docker
        setContainerStats({
          total: 5,
          running: 5,
          healthy: 5,
          unhealthy: 0
        });
      } catch (error) {
        console.error('Error checking container health:', error);
      }
    };

    checkContainerHealth();
    const interval = setInterval(checkContainerHealth, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy': return 'OK';
      case 'unhealthy': return 'ERROR';
      case 'starting': return 'INICIANDO';
      default: return 'DESCONOCIDO';
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      proxy: '#e74c3c',
      frontend: '#2ecc71',
      backend: '#f39c12',
      service: '#9b59b6',
      database: '#3498db'
    };
    return colors[category] || '#95a5a6';
  };

  return (
    <div className="docker-diagram">
      <div className="diagram-header">
        <h2>Arquitectura Docker</h2>
        <p>Vista interactiva de la aplicación TODO containerizada</p>
      </div>

      {/* Statistics Dashboard */}
      <div className="stats-dashboard">
        <div className="stat-card">
          <div className="stat-number">{containerStats.total}</div>
          <div className="stat-label">Total Contenedores</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{containerStats.running}</div>
          <div className="stat-label">Ejecutándose</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{containerStats.healthy}</div>
          <div className="stat-label">Saludables</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{containerStats.unhealthy}</div>
          <div className="stat-label">Problemas</div>
        </div>
      </div>

      {/* Services Grid */}
      <div className="services-grid">
        {services.map((service) => (
          <div 
            key={service.id} 
            className={`service-card ${service.category}`}
            style={{ borderLeftColor: getCategoryColor(service.category) }}
          >
            <div className="service-header">
              <div className="service-name">{service.name}</div>
              <div className="service-status">
                {getStatusIcon(service.status)}
              </div>
            </div>
            
            <div className="service-details">
              <div className="detail-row">
                <span className="detail-label">Container:</span>
                <span className="detail-value">{service.container}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Image:</span>
                <span className="detail-value">{service.image}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Port:</span>
                <span className="port-badge">:{service.port}</span>
              </div>
            </div>
            
            <div className="service-description">
              {service.description}
            </div>

            {service.connections.length > 0 && (
              <div className="service-connections">
                <span className="connections-label">Connects to:</span>
                <div className="connections-list">
                  {service.connections.map((conn) => (
                    <span key={conn} className="connection-tag">
                      {conn}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Docker Features */}
      <div className="features-section">
        <h3>Características Docker Implementadas</h3>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <div className="feature-title">{feature.title}</div>
              <div className="feature-description">{feature.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture Flow */}
      <div className="architecture-flow">
        <h3>Flujo de Solicitudes</h3>
        <div className="flow-diagram">
          <div className="flow-step">
            <div className="flow-icon">USER</div>
            <div className="flow-label">Usuario</div>
          </div>
          <div className="flow-arrow">→</div>
          <div className="flow-step">
            <div className="flow-icon">PROXY</div>
            <div className="flow-label">Nginx<br/>:80</div>
          </div>
          <div className="flow-arrow">→</div>
          <div className="flow-step">
            <div className="flow-icon">WEB</div>
            <div className="flow-label">React<br/>:3000</div>
          </div>
          <div className="flow-arrow">→</div>
          <div className="flow-step">
            <div className="flow-icon">API</div>
            <div className="flow-label">Flask API<br/>:5000</div>
          </div>
          <div className="flow-arrow">→</div>
          <div className="flow-step">
            <div className="flow-icon">DB</div>
            <div className="flow-label">MySQL<br/>:3306</div>
          </div>
        </div>
        
        <div className="flow-legend">
          <div className="legend-item">
            <span className="legend-icon">SEC</span>
            <span className="legend-text">Docker Secrets gestionan todas las credenciales sensibles</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon">HEALTH</span>
            <span className="legend-text">Health checks aseguran la disponibilidad de servicios</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon">GUARD</span>
            <span className="legend-text">Todos los contenedores se ejecutan como usuarios no-root</span>
          </div>
        </div>
      </div>

      {/* Command Reference */}
      <div className="commands-section">
        <h3>Comandos Docker</h3>
        <div className="commands-grid">
          <div className="command-card">
            <div className="command-title">Iniciar Todos los Servicios</div>
            <code className="command-code">./deploy.sh</code>
          </div>
          <div className="command-card">
            <div className="command-title">Detener Todos los Servicios</div>
            <code className="command-code">./stop.sh</code>
          </div>
          <div className="command-card">
            <div className="command-title">Ver Estado</div>
            <code className="command-code">docker-compose ps</code>
          </div>
          <div className="command-card">
            <div className="command-title">Ver Logs</div>
            <code className="command-code">docker-compose logs -f</code>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DockerDiagram;
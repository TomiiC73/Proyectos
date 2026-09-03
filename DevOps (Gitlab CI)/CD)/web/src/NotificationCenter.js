import React, { useState } from 'react';
import './NotificationCenter.css';
import BouncyLoader from './BouncyLoader';
import './BouncyLoader.css';

const NotificationCenter = ({ todos }) => {
  const [recipient, setRecipient] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const generateTaskReport = () => {
    const completedTasks = todos.filter(todo => todo.completed);
    const pendingTasks = todos.filter(todo => !todo.completed);
    const progress = todos.length > 0 ? Math.round((completedTasks.length / todos.length) * 100) : 0;
    const currentDate = new Date().toLocaleDateString('es-ES', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });

    const generateTaskList = (tasks, isCompleted = false) => {
      if (tasks.length === 0) {
        return `
          <tr>
            <td style="text-align: center; padding: 30px; background: ${isCompleted ? '#f8fafc' : '#fafafa'}; border-radius: 8px; color: ${isCompleted ? '#059669' : '#6b7280'}; font-size: 16px; font-weight: 500;">
              ${isCompleted ? 'Todas las tareas han sido completadas exitosamente' : 'No hay tareas pendientes en este momento'}
            </td>
          </tr>
        `;
      }

      return tasks.map((todo, index) => `
        <tr>
          <td style="padding: 16px 24px; border-bottom: 1px solid #f1f5f9; background: white;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td width="40" style="vertical-align: top; padding-right: 16px;">
                  <div style="width: 32px; height: 32px; border-radius: 6px; background: ${isCompleted ? '#059669' : '#0891b2'}; color: white; text-align: center; line-height: 32px; font-size: 14px; font-weight: 600;">
                    ${isCompleted ? '√' : index + 1}
                  </div>
                </td>
                <td style="vertical-align: middle;">
                  <div style="font-size: 16px; font-weight: 500; color: #1f2937; line-height: 1.5; ${isCompleted ? 'text-decoration: line-through; color: #6b7280;' : ''}">${todo.title}</div>
                  ${isCompleted ? '<div style="font-size: 12px; color: #059669; margin-top: 4px; font-weight: 500;">COMPLETADA</div>' : '<div style="font-size: 12px; color: #0891b2; margin-top: 4px; font-weight: 500;">PENDIENTE</div>'}
                </td>
              </tr>
            </table>
          </td>
        </tr>
      `).join('');
    };

    return `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Tareas - TODO App</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        @media only screen and (max-width: 600px) {
            .mobile-hide { display: none !important; }
            .mobile-center { text-align: center !important; }
            .mobile-padding { padding: 20px !important; }
            .mobile-stats { display: block !important; }
            .mobile-stat-card { margin: 10px 0 !important; }
        }
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    
    <!-- Email Container -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8fafc; padding: 40px 20px;">
        <tr>
            <td align="center">
                
                <!-- Main Content -->
                <table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08); overflow: hidden;">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%); color: white; padding: 40px 40px 40px 40px; text-align: center;">
                            <h1 style="margin: 0 0 20px 0; font-size: 32px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.2;">Reporte de Tareas</h1>
                            <div style="padding: 8px 16px; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 8px; display: inline-block;">
                                <span style="font-size: 14px; font-weight: 500; color: #38bdf8;">${currentDate}</span>
                            </div>
                        </td>
                    </tr>

                    <!-- Executive Summary -->
                    <tr>
                        <td style="background: #f1f5f9; padding: 35px 40px; border-bottom: 1px solid #e2e8f0;">
                            <!-- Progress Circle -->
                            <div style="text-align: center; margin-bottom: 30px;">
                                <div style="display: inline-block; position: relative; width: 140px; height: 140px;">
                                    <svg width="140" height="140" viewBox="0 0 140 140" style="transform: rotate(-90deg);">
                                        <circle cx="70" cy="70" r="60" fill="none" stroke="#e5e7eb" stroke-width="8"/>
                                        <circle cx="70" cy="70" r="60" fill="none" stroke="#0891b2" stroke-width="8" 
                                                stroke-dasharray="${2 * Math.PI * 60}" 
                                                stroke-dashoffset="${2 * Math.PI * 60 * (1 - progress / 100)}" 
                                                stroke-linecap="round"/>
                                    </svg>
                                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                                        <div style="font-size: 28px; font-weight: 700; color: #0891b2;">${progress}%</div>
                                        <div style="font-size: 12px; font-weight: 500; color: #64748b; margin-top: 2px;">COMPLETADO</div>
                                    </div>
                                </div>
                            </div>

                            <!-- Stats -->
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr class="mobile-stats">
                                    <td width="33.33%" align="center" style="padding: 20px 15px; background: white; border-radius: 12px; margin-right: 8px;" class="mobile-stat-card">
                                        <div style="font-size: 32px; font-weight: 700; color: #059669; margin-bottom: 6px;">${completedTasks.length}</div>
                                        <div style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px;">Completadas</div>
                                    </td>
                                    <td width="8" class="mobile-hide"></td>
                                    <td width="33.33%" align="center" style="padding: 20px 15px; background: white; border-radius: 12px; margin: 0 4px;" class="mobile-stat-card">
                                        <div style="font-size: 32px; font-weight: 700; color: #0891b2; margin-bottom: 6px;">${pendingTasks.length}</div>
                                        <div style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px;">Pendientes</div>
                                    </td>
                                    <td width="8" class="mobile-hide"></td>
                                    <td width="33.33%" align="center" style="padding: 20px 15px; background: white; border-radius: 12px; margin-left: 8px;" class="mobile-stat-card">
                                        <div style="font-size: 32px; font-weight: 700; color: #475569; margin-bottom: 6px;">${todos.length}</div>
                                        <div style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px;">Total</div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Completed Tasks Section -->
                    <tr>
                        <td style="padding: 35px 40px 20px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td>
                                        <h3 style="margin: 0 0 20px 0; font-size: 18px; font-weight: 600; color: #059669;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background: #059669; border-radius: 6px; color: white; text-align: center; line-height: 28px; font-size: 16px; font-weight: 700; margin-right: 12px;">√</span>
                                            Tareas Completadas (${completedTasks.length})
                                        </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; overflow: hidden;">
                                            ${generateTaskList(completedTasks, true)}
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Pending Tasks Section -->
                    <tr>
                        <td style="padding: 20px 40px 35px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td>
                                        <h3 style="margin: 0 0 20px 0; font-size: 18px; font-weight: 600; color: #0891b2;">
                                            <span style="display: inline-block; width: 28px; height: 28px; background: #0891b2; border-radius: 6px; color: white; text-align: center; line-height: 28px; font-size: 16px; font-weight: 700; margin-right: 12px;">•</span>
                                            Tareas Pendientes (${pendingTasks.length})
                                        </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; overflow: hidden;">
                                            ${generateTaskList(pendingTasks, false)}
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background: #0f172a; color: #e2e8f0; padding: 30px 40px; text-align: center;">
                            <div style="border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 20px;">
                                <h4 style="margin: 0; font-size: 16px; font-weight: 600; color: white;">TODO App</h4>
                                <p style="margin: 6px 0 0 0; font-size: 14px; color: #94a3b8; font-weight: 400;">Aplicación de Gestión de Tareas</p>
                            </div>
                            <p style="margin: 0; font-size: 12px; color: #64748b; line-height: 1.5;">
                                Este reporte fue generado automáticamente el ${new Date().toLocaleString('es-ES')}<br>
                                Aplicación desarrollada con tecnologías modernas: React, Flask y Docker
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    `;
  };

  const handleSendTaskReport = async () => {
    if (!recipient.trim()) {
      alert('Por favor ingresa un email válido');
      return;
    }

    // Validación básica de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(recipient.trim())) {
      alert('Por favor ingresa un email válido');
      return;
    }

    setIsLoading(true);
    try {
      const taskReport = generateTaskReport();
      
      const response = await fetch('/notifications/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'email',
          recipient: recipient.trim(),
          message: taskReport,
          title: 'Reporte de Tareas - TODO App',
          isHtml: true
        }),
      });

      // Verificar si la respuesta es JSON válida
      let result;
      const contentType = response.headers.get('content-type');
      
      if (contentType && contentType.includes('application/json')) {
        try {
          result = await response.json();
        } catch (jsonError) {
          throw new Error('Respuesta del servidor no es JSON válido');
        }
      } else {
        // Si no es JSON, obtener el texto de la respuesta
        const text = await response.text();
        console.log('Respuesta del servidor:', text);
        
        if (response.ok) {
          alert('¡Reporte de tareas enviado exitosamente por email!');
          setRecipient('');
          return;
        } else {
          throw new Error(`Error del servidor: ${response.status} - ${text}`);
        }
      }

      if (response.ok) {
        alert('¡Reporte de tareas enviado exitosamente por email! 📧');
        setRecipient('');
      } else {
        const errorText = result?.detail || result?.message || `Error del servidor: ${response.status}`;
        alert(`❌ Error enviando email: ${errorText}`);
      }
    } catch (error) {
      console.error('Error completo:', error);
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        alert('❌ Error de conexión: No se puede conectar al servicio de notificaciones. Verifica que todos los servicios estén ejecutándose.');
      } else {
        alert(`❌ Error: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="notification-panel-static">
      <div className="panel-header">
        <h3>Centro de Notificaciones</h3>
        <p style={{margin: 0, fontSize: '0.9rem', opacity: 0.9}}>Gestiona las notificaciones de tus tareas</p>
      </div>

        <div className="notification-content">
          <div className="info-section">
            <h4>Reporte de Tareas por Correo Electrónico</h4>
            <p>Envía un resumen completo de tus tareas completadas y pendientes a cualquier dirección de correo electrónico. El reporte incluye estadísticas detalladas y el progreso de tus tareas.</p>
          </div>

          <div className="form-group">
            <label htmlFor="recipient">Correo electrónico destinatario:</label>
            <input
              id="recipient"
              type="email"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              placeholder="ejemplo@correo.com"
              className="form-input"
              disabled={isLoading}
            />
          </div>

          <div className="preview-section">
            <h5>Vista previa del reporte:</h5>
            <div className="report-preview">
              {todos ? (
                <>
                  <div className="preview-stats">
                    <span className="stat completed">Completadas: {todos.filter(t => t.completed).length}</span>
                    <span className="stat pending">Pendientes: {todos.filter(t => !t.completed).length}</span>
                    <span className="stat total">Total: {todos.length}</span>
                  </div>
                </>
              ) : (
                <p>Cargando tareas...</p>
              )}
            </div>
          </div>

          <button
            onClick={handleSendTaskReport}
            disabled={isLoading}
            className="send-btn"
          >
            {isLoading ? (
              <div className="loading-with-bouncy">
                <BouncyLoader size={16} color="#ffffff" speed={1.2} />
                <span>Enviando reporte...</span>
              </div>
            ) : (
              'Enviar Reporte por Correo Electrónico'
            )}
          </button>
        </div>
    </div>
  );
};

export default NotificationCenter;
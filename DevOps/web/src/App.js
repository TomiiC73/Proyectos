import React, { useState, useEffect } from 'react';
import './App.css';
import NotificationCenter from './NotificationCenter';
import DockerDiagram from './DockerDiagram';
import BouncyLoader from './BouncyLoader';
import './BouncyLoader.css';

const API_BASE_URL = '/api';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('todos'); // Nueva state para tabs

  // Cargar todos desde la API
  const loadTodos = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/todos`);
      if (response.ok) {
        const data = await response.json();
        setTodos(data);
        setError('');
      } else {
        throw new Error('Error al cargar las tareas');
      }
    } catch (err) {
      setError('Error cargando tareas: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Agregar nuevo todo
  const addTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTodo.trim() }),
      });

      if (response.ok) {
        const newTodoItem = await response.json();
        setTodos([...todos, newTodoItem]);
        setNewTodo('');
        setError('');
      } else {
        throw new Error('Error al agregar tarea');
      }
    } catch (err) {
      setError('Error agregando tarea: ' + err.message);
    }
  };

  // Marcar todo como completado
  const toggleTodo = async (id) => {
    try {
      const todo = todos.find(t => t.id === id);
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !todo.completed }),
      });

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(t => t.id === id ? updatedTodo : t));
        setError('');
      } else {
        throw new Error('Error al actualizar tarea');
      }
    } catch (err) {
      setError('Error actualizando tarea: ' + err.message);
    }
  };

  // Eliminar todo
  const deleteTodo = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setTodos(todos.filter(t => t.id !== id));
        setError('');
      } else {
        throw new Error('Error al eliminar tarea');
      }
    } catch (err) {
      setError('Error eliminando tarea: ' + err.message);
    }
  };

  // Cargar datos al montar el componente
  useEffect(() => {
    loadTodos();
  }, []);

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1 className="app-title">Lista de Tareas</h1>
          <div className="status-bar">
            <div className="status-item">
              <span>Total Tareas: </span>
              <span className="status-value">{todos.length}</span>
            </div>
            <div className="status-item">
              <span>Completadas: </span>
              <span className="status-value">{todos.filter(t => t.completed).length}</span>
            </div>
          </div>
        </header>

        {/* Navegación por pestañas */}
        <nav className="tab-navigation">
          <button 
            className={`tab-btn ${activeTab === 'todos' ? 'primary' : 'outline'}`}
            onClick={() => setActiveTab('todos')}
          >
            Lista de Tareas
          </button>
          <button 
            className={`tab-btn ${activeTab === 'docker' ? 'primary' : 'outline'}`}
            onClick={() => setActiveTab('docker')}
          >
            Arquitectura Docker
          </button>
          <button 
            className={`tab-btn ${activeTab === 'notifications' ? 'primary' : 'outline'}`}
            onClick={() => setActiveTab('notifications')}
          >
            Notificaciones
          </button>
        </nav>

        <main className="main-content">
          {/* Contenido de la pestaña Todo List */}
          {activeTab === 'todos' && (
            <div className="tab-content">
              {error && (
                <div className="error-message">
                  <span>⚠ {error}</span>
                  <button onClick={loadTodos} className="retry-btn">Reintentar</button>
                </div>
              )}

          <div className="form-card">
            <form onSubmit={addTodo} className="add-todo-form">
              <input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="Agregar nueva tarea..."
                className="todo-input"
                disabled={loading}
              />
              <button 
                type="submit" 
                className="btn primary"
                disabled={loading || !newTodo.trim()}
              >
                ✨ Agregar Tarea
              </button>
            </form>
          </div>

          <div className="todos-container">
            {loading ? (
              <div className="loading-with-bouncy">
                <BouncyLoader 
                  size="50" 
                  speed="1.75" 
                  color="#667eea" 
                />
                <p className="loading-text">Cargando tareas...</p>
              </div>
            ) : todos.length === 0 ? (
              <div className="empty-state">
                <h3>No hay tareas aún</h3>
                <p>Agrega tu primera tarea arriba para comenzar.</p>
              </div>
            ) : (
              <div className="todos-list">
                {todos.map((todo) => (
                  <div 
                    key={todo.id}
                    className={`todo-item ${todo.completed ? 'completed' : ''}`}
                  >
                    <div className="todo-content">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => toggleTodo(todo.id)}
                        className="todo-checkbox"
                      />
                      <span className="todo-text">{todo.title}</span>
                      {todo.created_at && (
                        <span className="todo-date">
                          {new Date(todo.created_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="delete-btn"
                      title="Eliminar tarea"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="3,6 5,6 21,6"></polyline>
                        <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
              </div>
            </div>
          )}

          {/* Contenido de la pestaña Docker Architecture */}
          {activeTab === 'docker' && (
            <div className="tab-content">
              <DockerDiagram />
            </div>
          )}

          {/* Contenido de la pestaña Notifications */}
          {activeTab === 'notifications' && (
            <div className="tab-content">
              <NotificationCenter todos={todos} />
            </div>
          )}
        </main>

        <footer className="footer">
          <p>Aplicación de Tareas Dockerizada - Construida con React y Flask</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

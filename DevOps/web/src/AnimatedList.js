import React, { useEffect, useRef } from 'react';
import anime from 'animejs/lib/anime.es.js';
import './AnimatedList.css';

const AnimatedList = ({ children, className = '' }) => {
  const listRef = useRef(null);

  useEffect(() => {
    if (listRef.current) {
      const items = listRef.current.querySelectorAll('.animated-list-item');
      
      // Animar entrada de elementos de lista
      anime({
        targets: items,
        translateX: [50, 0],
        opacity: [0, 1],
        duration: 600,
        delay: anime.stagger(100), // 100ms de retraso entre cada elemento
        easing: 'easeOutCubic'
      });
    }
  }, [children]);

  return (
    <div ref={listRef} className={`animated-list ${className}`}>
      {React.Children.map(children, (child, index) => (
        <div 
          key={index} 
          className="animated-list-item"
          style={{ opacity: 0, transform: 'translateX(50px)' }}
        >
          {child}
        </div>
      ))}
    </div>
  );
};

// Componente especializado para elementos de tarea
export const AnimatedTodoItem = ({ 
  todo, 
  onToggle, 
  onDelete, 
  isNew = false 
}) => {
  const itemRef = useRef(null);

  useEffect(() => {
    if (itemRef.current && isNew) {
      // Animación especial para nuevos elementos
      anime({
        targets: itemRef.current,
        scale: [0.8, 1.05, 1],
        opacity: [0, 1],
        duration: 600,
        easing: 'easeOutBack'
      });
    }
  }, [isNew]);

  const handleToggle = () => {
    // Animación de toggle
    anime({
      targets: itemRef.current,
      rotateY: [0, 360],
      duration: 500,
      easing: 'easeInOutQuad',
      complete: () => onToggle(todo.id)
    });
  };

  const handleDelete = () => {
    // Animación de eliminación
    anime({
      targets: itemRef.current,
      translateX: [0, 100],
      opacity: [1, 0],
      scale: [1, 0.8],
      duration: 400,
      easing: 'easeInBack',
      complete: () => onDelete(todo.id)
    });
  };

  const handleMouseEnter = () => {
    anime({
      targets: itemRef.current,
      translateX: [0, 5],
      boxShadow: ['0 2px 8px rgba(0,0,0,0.1)', '0 8px 25px rgba(0,0,0,0.15)'],
      duration: 200,
      easing: 'easeOutQuad'
    });
  };

  const handleMouseLeave = () => {
    anime({
      targets: itemRef.current,
      translateX: [5, 0],
      boxShadow: ['0 8px 25px rgba(0,0,0,0.15)', '0 2px 8px rgba(0,0,0,0.1)'],
      duration: 200,
      easing: 'easeOutQuad'
    });
  };

  return (
    <div 
      ref={itemRef}
      className={`animated-todo-item ${todo.completed ? 'completed' : ''}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="todo-content">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={handleToggle}
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
        onClick={handleDelete}
        className="delete-btn animated-delete-btn"
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
  );
};

export default AnimatedList;
import React, { useRef, useEffect } from 'react';
import anime from 'animejs/lib/anime.es.js';
import './AnimatedButton.css';

const AnimatedButton = ({ 
  children, 
  onClick, 
  className = '', 
  variant = 'primary',
  disabled = false,
  loading = false,
  type = 'button'
}) => {
  const buttonRef = useRef(null);
  const rippleRef = useRef(null);

  useEffect(() => {
    if (buttonRef.current) {
      // Animación de entrada suave
      anime({
        targets: buttonRef.current,
        scale: [0.95, 1],
        opacity: [0, 1],
        duration: 500,
        easing: 'easeOutBack'
      });
    }
  }, []);

  const handleClick = (e) => {
    if (disabled || loading) return;

    // Efecto ripple
    const button = buttonRef.current;
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    const ripple = document.createElement('span');
    ripple.className = 'ripple-effect';
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    button.appendChild(ripple);

    // Animar el ripple
    anime({
      targets: ripple,
      scale: [0, 2],
      opacity: [0.5, 0],
      duration: 600,
      easing: 'easeOutQuart',
      complete: () => ripple.remove()
    });

    // Animación de click del botón
    anime({
      targets: button,
      scale: [1, 0.95, 1],
      duration: 200,
      easing: 'easeOutQuad'
    });

    if (onClick) onClick(e);
  };

  const handleMouseEnter = () => {
    if (disabled || loading) return;
    
    anime({
      targets: buttonRef.current,
      translateY: [0, -2],
      boxShadow: ['0 2px 8px rgba(0,0,0,0.1)', '0 6px 20px rgba(0,0,0,0.15)'],
      duration: 200,
      easing: 'easeOutQuad'
    });
  };

  const handleMouseLeave = () => {
    if (disabled || loading) return;
    
    anime({
      targets: buttonRef.current,
      translateY: [-2, 0],
      boxShadow: ['0 6px 20px rgba(0,0,0,0.15)', '0 2px 8px rgba(0,0,0,0.1)'],
      duration: 200,
      easing: 'easeOutQuad'
    });
  };

  return (
    <button
      ref={buttonRef}
      type={type}
      className={`animated-button ${variant} ${className} ${disabled ? 'disabled' : ''} ${loading ? 'loading' : ''}`}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      disabled={disabled || loading}
      style={{ opacity: 0 }}
    >
      <span className="button-content">
        {children}
      </span>
    </button>
  );
};

export default AnimatedButton;
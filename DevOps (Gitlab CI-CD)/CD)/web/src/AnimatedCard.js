import React, { useEffect, useRef } from 'react';
import anime from 'animejs/lib/anime.es.js';
import './AnimatedCard.css';

const AnimatedCard = ({ children, delay = 0, className = '' }) => {
  const cardRef = useRef(null);

  useEffect(() => {
    if (cardRef.current) {
      // Animación de entrada
      anime({
        targets: cardRef.current,
        translateY: [30, 0],
        opacity: [0, 1],
        duration: 800,
        delay: delay,
        easing: 'easeOutCubic'
      });
    }
  }, [delay]);

  const handleHover = () => {
    anime({
      targets: cardRef.current,
      scale: [1, 1.03],
      duration: 300,
      easing: 'easeOutQuad'
    });
  };

  const handleHoverOut = () => {
    anime({
      targets: cardRef.current,
      scale: [1.03, 1],
      duration: 300,
      easing: 'easeOutQuad'
    });
  };

  return (
    <div 
      ref={cardRef}
      className={`animated-card ${className}`}
      onMouseEnter={handleHover}
      onMouseLeave={handleHoverOut}
      style={{ opacity: 0 }}
    >
      {children}
    </div>
  );
};

export default AnimatedCard;
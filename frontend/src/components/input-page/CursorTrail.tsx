import { useEffect, useState } from 'react';

const CursorTrail = ({ position }) => {
  const [trails, setTrails] = useState([]);

  useEffect(() => {
    // Only create trail at random intervals
    if (Math.random() > 0.1) return;
    
    // Create a new trail dot
    const newTrail = {
      id: Date.now(),
      x: position.x,
      y: position.y,
      color: Math.random() > 0.5 ? 'var(--primary-color)' : 'var(--secondary-color)'
    };
    
    // Add the new trail
    setTrails(prevTrails => [...prevTrails, newTrail]);
    
    // Remove the trail after animation
    setTimeout(() => {
      setTrails(prevTrails => prevTrails.filter(trail => trail.id !== newTrail.id));
    }, 500);
  }, [position]);

  return (
    <>
      {trails.map(trail => (
        <div
          key={trail.id}
          className="cursor-trail"
          style={{
            left: `${trail.x}px`,
            top: `${trail.y}px`,
            backgroundColor: trail.color
          }}
        />
      ))}
    </>
  );
};

export default CursorTrail;

import Content from "@/components/input-page/Content";
import CursorTrail from "@/components/input-page/CursorTrail";
import { useCallback, useEffect, useState } from "react";

export function Input() {
    const [formVisible, setFormVisible] = useState(true);
    const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  
    const playSound = useCallback(() => {
      // Create audio element
      const audio = new Audio();
      audio.volume = 0.5;
      
      // Use a modern sci-fi sound
      audio.src = 'https://assets.mixkit.co/active_storage/sfx/209/209-preview.mp3';
      
      // Play the sound
      audio.play().catch(error => {
        console.warn('Audio could not be played:', error);
      });
    }, []);

    const hideEntryForm = useCallback(() => {
      // Hide the entry form
      setFormVisible(false);
      
      // Play sound effect
      playSound();
    }, [playSound]);
  
    const handleSubmit = useCallback((accessCode) => {
      // Set visited flag in localStorage
      localStorage.setItem('hasVisited', 'true');
      
      // Hide entry form after verification
      setTimeout(() => {
        hideEntryForm();
      }, 800);
    }, [hideEntryForm]);

    const handleMouseMove = useCallback((e: MouseEvent) => {
      setCursorPosition({ x: e.pageX, y: e.pageY });
    }, []);
  
    useEffect(() => {
      // Check if this is first visit
      const hasVisited = localStorage.getItem('hasVisited');
      
      if (hasVisited) {
        // If already visited, show content immediately
        setTimeout(() => {
          hideEntryForm();
        }, 500);
      }

      // Add cursor trail effect
      window.addEventListener('mousemove', handleMouseMove);
      
      return () => {
        window.removeEventListener('mousemove', handleMouseMove);
      };
    }, [hideEntryForm, handleMouseMove]);
  
    return (
      <div className="container w-screen h-screen overflow-hidden p-0 m-0">
        <Content />
        <CursorTrail position={cursorPosition} />
      </div>
    );
}
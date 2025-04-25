import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid'; 

const LOCAL_STORAGE_KEY = 'anonymousUserId'; // Use a descriptive key

function useUserId() {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    let storedUserId = localStorage.getItem(LOCAL_STORAGE_KEY);

    if (storedUserId) {
      setUserId(storedUserId);
      console.log('Retrieved user ID from localStorage:', storedUserId);
    } else {
      const newUserId = uuidv4();
      try {
        localStorage.setItem(LOCAL_STORAGE_KEY, newUserId);
        setUserId(newUserId);
        console.log('Generated and stored new anonymous user ID:', newUserId);
      } catch (error) {
        // Handle potential localStorage errors (e.g., private browsing mode)
        console.error("Error saving user ID to localStorage:", error);
        // Still set the ID for the current session, but it won't persist
        setUserId(newUserId);
        console.log('Generated ephemeral anonymous user ID (localStorage failed):', newUserId);
      }
    }
  }, []); 

  return userId;
}

export default useUserId;
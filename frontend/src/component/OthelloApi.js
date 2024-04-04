const API_URL = 'YOUR_API_URL_HERE'; // Replace with your API URL

export const sendGameState = async (gameState) => {
 try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(gameState),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
 } catch (error) {
    console.error('There was a problem with your fetch operation:', error);
 }
};

const API_ENDPOINT = '/magic';

/**
 * Sends an image to the server for processing.
 * @param {string} image - Base64 encoded image data.
 * @returns {Promise<Object>} The processed image data.
 * @throws {Error} If the network response is not ok.
 */
async function magic(image) {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error in magic function:', error);
    throw error;
  }
}


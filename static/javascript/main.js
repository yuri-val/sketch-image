document.addEventListener('DOMContentLoaded', () => {
  const magicButton = document.getElementById('magic-button');
  const magicImage = document.getElementById('magic-image');
  const imageDescription = document.getElementById('image-description');
  const imageUUID = document.getElementById('image-uuid');
  const converter = new showdown.Converter();

  function resetUI() {
    magicImage.src = '';
    magicImage.hidden = true;
    imageDescription.innerHTML = '';
    magicImage.classList.add('loader');
    magicButton.disabled = true;
    magicButton.classList.add('loading');
  }

  function updateUI(response) {
    magicImage.src = response.image;
    magicImage.hidden = false;
    magicImage.classList.remove('loader');
    imageUUID.textContent = response.uuid;
    imageDescription.innerHTML = converter.makeHtml(response.description);
    magicButton.disabled = false;
    magicButton.classList.remove('loading');
  }

  magicButton.addEventListener('click', async () => {
    resetUI();

    const canvas = document.querySelector("#drawing-tool canvas.lower-canvas");
    const base64image = canvas.toDataURL("image/png");

    try {
      const response = await magic(base64image);
      updateUI(response);
    } catch (error) {
      console.error('Error processing image:', error);
      imageDescription.textContent = 'An error occurred while processing the image.';
      magicButton.disabled = false;
      magicButton.classList.remove('loading');
    }
  });
});
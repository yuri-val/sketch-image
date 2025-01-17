async function magic(image) {
  const response = await fetch('/magic', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image })
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return await response.json();
}

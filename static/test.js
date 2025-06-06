const card = document.createElement('img');

// Set default image first
document.body.appendChild(card);

// Fetch the JSON data
fetch('/static/blackjack_cards.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        //* Code here
        console.log('Fetched data:', data);
        card.src = data[Math.floor(Math.random() * 52)]['image']
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
        // You could set a fallback image here if needed
        // card.src = '/static/cards/fallback.png';
    });

console.log('bar'); // This will log before fetch completes
// --- Autocomplete Functionality ---
// Fetch the full movie list when the page loads to populate autocomplete
window.onload = async function() {
    try {
        const response = await fetch('/movies');
        const movieTitles = await response.json();
        const datalist = document.getElementById('movie-titles');

        movieTitles.forEach(title => {
            const option = document.createElement('option');
            option.value = title;
            datalist.appendChild(option);
        });
    } catch (error) {
        console.error("Failed to load movie list for autocomplete:", error);
    }
};

// --- Recommendation Functionality ---
async function getRecommendations() {
    const movieTitle = document.getElementById('movieInput').value;
    const resultContainer = document.getElementById('result');
    
    // Show the CSS spinner
    resultContainer.innerHTML = '<div class="loader"></div>';

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie: movieTitle })
        });

        const data = await response.json();
        resultContainer.innerHTML = ''; // Clear the spinner

        if (data.error) {
            resultContainer.innerHTML = `<p style="color: var(--secondary-text-color);">${data.error}</p>`;
        } else {
            data.recommendations.forEach(movie => {
                const movieCard = `
                    <div class="movie-card">
                        <img src="${movie.poster_url}" alt="${movie.title} Poster">
                        <p>${movie.title}</p>
                    </div>
                `;
                resultContainer.innerHTML += movieCard;
            });
        }
    } catch (error) {
        resultContainer.innerHTML = `<p style="color: var(--secondary-text-color);">Could not connect to the server. Please make sure it's running.</p>`;
        console.error("Error fetching recommendations:", error);
    }
}
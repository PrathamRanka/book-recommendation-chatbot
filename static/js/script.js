// filepath: book-recommendation-chatbot/book-recommendation-chatbot/static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('user-input');
  const chatBox = document.getElementById('chat-box');
  const genreFilter = document.getElementById('genre-filter');
  const priceRange = document.getElementById('price-range');
  const ratingFilter = document.getElementById('rating-filter');
  const bestsellerToggle = document.getElementById('bestseller-toggle');
  const sortFilter = document.getElementById('sort-filter');

  input.addEventListener('input', function() {
    const query = input.value.trim();
    if (query) {
      fetchChatRecommendations(query);
      clearSuggestions();
    } else {
      fetchRecommendations();
    }
  });

  genreFilter.addEventListener('change', function() {
    fetchRecommendations();
  });

  // On page load, show all books
  fetchRecommendations();

  priceRange.addEventListener('input', function() {
    document.getElementById('price-value').textContent = '₹' + priceRange.value;
    fetchRecommendations();
  });

  ratingFilter.addEventListener('change', function() {
    fetchRecommendations();
  });

  bestsellerToggle.addEventListener('change', function() {
    fetchRecommendations();
  });

  sortFilter.addEventListener('change', fetchRecommendations);

  async function fetchSuggestions(query) {
    const res = await fetch(`/suggestions?query=${encodeURIComponent(query)}`);
    const suggestions = await res.json();
    displaySuggestions(suggestions);
  }

  function displaySuggestions(suggestions) {
    clearSuggestions();
    suggestions.forEach(s => {
      const suggestionDiv = document.createElement('div');
      suggestionDiv.textContent = s.name;
      suggestionDiv.classList.add('suggestion-item');
      suggestionDiv.onclick = () => {
        input.value = s.name;
        clearSuggestions();
      };
      chatBox.appendChild(suggestionDiv);
    });
  }

  function clearSuggestions() {
    const suggestionItems = document.querySelectorAll('.suggestion-item');
    suggestionItems.forEach(item => item.remove());
  }

  async function fetchRecommendations() {
    let maxPrice = priceRange.value;
    // If slider is at 0, send null to backend to mean "no price filter"
    if (parseInt(maxPrice) === 0) {
      maxPrice = null;
    }
    const filters = {
      genre: genreFilter.value,
      min_price: 0,
      max_price: maxPrice,
      rating: ratingFilter.value,
      bestseller: bestsellerToggle.checked,
      sort: sortFilter.value
    };

    const res = await fetch('/recommendations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(filters)
    });
    const recommendations = await res.json();
    displayRecommendations(recommendations);
  }

  async function fetchChatRecommendations(query) {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: query })
    });
    const data = await res.json();
    displayRecommendations(data.response);
  }

  function displayRecommendations(recommendations) {
    clearChatBox();
    recommendations.forEach(r => {
      const imgSrc = r.image.startsWith('http') ? r.image : `/static/${r.image}`;
      const msgDiv = document.createElement('div');
      msgDiv.className = 'book-card';
      msgDiv.innerHTML = `
        <div class="img-wrapper">
          <img src="${imgSrc}" alt="${r.name}" class="book-img" loading="lazy"/>
        </div>
        <div class="book-info">
          <strong>${r.name}</strong><br>
          <span>${r.price}</span> 
          <span class="star">⭐${r.rating}</span>
          ${r.bestseller ? '<span class="bestseller-tag">Bestseller</span>' : ''}
        </div>
      `;
      // Fade in image when loaded
      const img = msgDiv.querySelector('.book-img');
      img.onload = () => img.classList.add('loaded');
      chatBox.appendChild(msgDiv);
    });
  }

  function clearChatBox() {
    chatBox.innerHTML = '';
  }

  function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'You' ? 'message user' : 'message bot';
    msgDiv.innerHTML = `
      <div class="avatar">${sender === 'You' ? '🧑' : '🤖'}</div>
      <div class="bubble">${text}</div>
    `;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
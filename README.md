# Book Recommendation Chatbot

## Overview
The Book Recommendation Chatbot is an advanced application designed to provide personalized book recommendations based on user input, reading history, and preferences. The chatbot features a polished user interface with real-time search-as-you-type dropdowns, genre filters, price range selectors, user ratings, and bestseller tags.

## Features
- **Real-time Search**: Users can type in their queries and receive instant suggestions.
- **Genre Filters**: Users can filter recommendations based on their preferred genres.
- **Price Range Selector**: Users can specify their budget to receive relevant recommendations.
- **User Ratings**: Recommendations are influenced by user ratings and reviews.
- **Bestseller Tags**: Highlight popular books to help users discover trending titles.
- **Personalized Recommendations**: The chatbot analyzes user input and history to provide tailored suggestions.

## Project Structure
```
book-recommendation-chatbot
├── backend
│   ├── app.py                # Main entry point for the backend application
│   ├── chat_logic.py         # Logic for processing user messages and searching products
│   ├── recommender.py        # Recommendation logic based on user input and preferences
│   ├── models
│   │   └── user_model.py     # User model for managing user data and preferences
│   ├── data
│   │   ├── products.json     # Product data including book titles and prices
│   │   └── users.json        # User data including reading history and preferences
│   ├── requirements.txt      # Python dependencies for the backend application
│   └── templates
│       └── index.html        # Main user interface for the chatbot
├── static
│   ├── css
│   │   └── style.css         # Styles for the user interface
│   ├── js
│   │   └── script.js         # Frontend logic for the chatbot
│   └── fonts                 # Custom fonts for the user interface
└── README.md                 # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd book-recommendation-chatbot
   ```

2. Navigate to the backend directory and install the required dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and go to `http://127.0.0.1:5000` to access the chatbot interface.

## Usage
- Start a conversation with the chatbot by typing your queries in the input box.
- Use the filters and selectors to refine your book recommendations.
- Explore the suggestions provided by the chatbot based on your preferences.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
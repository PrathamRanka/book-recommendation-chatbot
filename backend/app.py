from flask import Flask, request, jsonify, render_template
import json
import os
from chat_logic import search_products
from recommender import get_recommendations

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    static_url_path='/static'
)

# Load product and user data once at start
with open(os.path.join(os.path.dirname(__file__), 'data', 'products.json'), 'r', encoding='utf-8') as f:
    PRODUCTS = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'data', 'users.json'), 'r', encoding='utf-8') as f:
    USERS = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')  # serves HTML UI

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '').lower()
    matches = search_products(user_msg, PRODUCTS)
    return jsonify({'response': matches})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_id = data.get('user_id')
    recommendations = get_recommendations(user_id, USERS, PRODUCTS)
    return jsonify({'recommendations': recommendations})

@app.route('/suggestions')
def suggestions():
    query = request.args.get('query', '').lower()
    # Return book titles that match the query (autocomplete)
    matches = [
        {'name': p['name']}
        for p in PRODUCTS
        if query in p['name'].lower()
    ][:5]
    return jsonify(matches)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    data = request.get_json()
    genre = data.get('genre')
    min_price = float(data.get('min_price', 0))
    max_price = data.get('max_price')
    rating = data.get('rating')
    bestseller = data.get('bestseller')
    sort = data.get('sort')

    results = PRODUCTS

    if genre:
        genre_map = {
            "non-fiction": ["Non-Fiction", "Memoir", "Self-Help", "Finance", "Business"],
            # ...other mappings...
        }
        allowed = genre_map.get(genre.lower(), [genre])
        results = [p for p in results if p.get('category', '').lower() in [g.lower() for g in allowed]]

    # Only filter by price if max_price is not None/null/empty string
    if max_price not in [None, '', 'null']:
        try:
            max_price = float(max_price)
        except Exception:
            max_price = 1000000
        filtered = []
        for p in results:
            try:
                price_val = float(str(p.get('price', '0')).replace('₹', '').replace(',', ''))
                if min_price <= price_val <= max_price:
                    filtered.append(p)
            except:
                continue
        results = filtered
    if rating:
        try:
            rating_val = float(rating)
            results = [p for p in results if p.get('rating', 0) >= rating_val]
        except:
            pass
    if bestseller is not None:
        if bestseller:
            results = [p for p in results if p.get('bestseller', False)]

    # Sort by price if requested
    if sort == "price-asc":
        results = sorted(results, key=lambda x: float(str(x.get('price', '0')).replace('₹', '').replace(',', '')))
    elif sort == "price-desc":
        results = sorted(results, key=lambda x: float(str(x.get('price', '0')).replace('₹', '').replace(',', '')), reverse=True)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
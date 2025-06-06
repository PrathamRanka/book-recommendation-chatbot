def get_user_preferences(user_id, users_data):
    user = next((u for u in users_data if u.get('user_id') == user_id), None)
    if user and 'preferences' in user:
        prefs = user['preferences']
        return {
            'genres': prefs.get('genres', []),
            'min_price': prefs.get('price_range', {}).get('min', 0),
            'max_price': prefs.get('price_range', {}).get('max', float('inf')),
            'ratings': prefs.get('ratings', [])
        }
    return None

def recommend_books(user_preferences, reading_history, products):
    recommended = []
    for product in products:
        # Genre filter
        if user_preferences['genres'] and product.get('category') not in user_preferences['genres']:
            continue
        # Price filter
        try:
            price = float(str(product.get('price', '0')).replace('₹', '').replace(',', ''))
        except Exception:
            price = 0
        if not (user_preferences['min_price'] <= price <= user_preferences['max_price']):
            continue
        # Rating filter
        if user_preferences['ratings'] and int(round(product.get('rating', 0))) not in user_preferences['ratings']:
            continue
        recommended.append(product)
    # Sort by rating and bestseller
    recommended.sort(key=lambda x: (not x.get('bestseller', False), -x.get('rating', 0)), reverse=False)
    return recommended  # Return all, not just top 10

def personalize_recommendations(user_id, products, users_data):
    user_preferences = get_user_preferences(user_id, users_data)
    if user_preferences:
        return recommend_books(user_preferences, [], products)
    return []

def get_recommendations(user_id, users, products):
    user_preferences = get_user_preferences(user_id, users)
    if user_preferences:
        return recommend_books(user_preferences, [], products)
    # Fallback: return all sorted by rating
    return sorted(products, key=lambda x: x.get('rating', 0), reverse=True)
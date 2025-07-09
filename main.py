from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

@app.route('/')
def home():
    return "✅ News Decoder API is running!"

@app.route('/news')
def get_news():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'error': 'Please provide a topic'}), 400

    url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize=5&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch news'}), 500

    data = response.json()

    headlines = []
    if 'articles' in data:
        for article in data['articles']:
            headlines.append({
                'source': article['source']['name'],
                'title': article['title']
            })

    return jsonify({
        'topic': topic,
        'headlines': headlines
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


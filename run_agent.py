

from flask import Flask, request, jsonify, render_template
import asyncio
from service_recommendation_agent import get_service_recommendations, conversation_history

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
async def get_recommendation():
    data = request.json
    query = data.get('query')
    recommendation = await get_service_recommendations(query, conversation_history)
    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True)
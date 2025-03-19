
# import asyncio
# from service_recommendation_agent import get_service_recommendations, conversation_history

# async def main():
#     print("Welcome to the Razorpay Service Recommender")
#     print("===========================================")
#     print("Type 'exit' to quit the application")
#     print("Type 'new' to start a new conversation")
    
#     while True:
#         user_input = input("\nDescribe what you need to accomplish: ")
        
#         if user_input.lower() == 'exit':
#             print("Thank you for using the Service Recommender. Goodbye!")
#             break
            
#         if user_input.lower() == 'new':
#             global conversation_history
#             conversation_history = [
#                 {"role": "system", "content": "You are a Razorpay internal service recommendation agent. Your task is to help employees find the right internal services for their tasks. Maintain context from previous messages in the conversation."}
#             ]
#             print("Started a new conversation!")
#             continue
        
#         try:
#             await get_service_recommendations(user_input, conversation_history)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(main())



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
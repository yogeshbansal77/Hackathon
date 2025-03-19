
import asyncio
import os
import datetime
from pathlib import Path
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    collection = chroma_client.get_collection("razorpay_services")
    print("Connected to existing collection")
except:
    print("Collection doesn't exist, please run populate_db.py first")
    exit(1)

# Create recommendations directory if it doesn't exist
recommendations_dir = Path("./recommendations")
recommendations_dir.mkdir(exist_ok=True)

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a Razorpay internal service recommendation agent. Your task is to help employees find the right internal services for their tasks. Maintain context from previous messages in the conversation."}
]

async def get_service_recommendations(query, history):
    # First, add the user's raw query to conversation history
    # This ensures clean history for context maintenance
    history.append({"role": "user", "content": query})
    
    # Search for services
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    services_info = []
    if 'documents' in results and results['documents']:
        documents = results['documents']
        print(f"Documents structure: {len(documents)} lists with {[len(d) for d in documents]} items")
        
        for doc_list in documents:
            if doc_list:  # Check if the list is not empty
                for doc in doc_list:
                    services_info.append(doc)
    
    if not services_info:
        print("No matching services found for your query")
        simple_response = "No matching services found."
        history.append({"role": "assistant", "content": simple_response})
        return simple_response
    
    services_text = "\n\n".join(services_info)
    
    # Prepare messages for API call, including conversation history and service info
    messages = history.copy()  # Start with existing conversation history
    
    # Add service information as a separate system message just for this API call
    # This won't be stored in the conversation history
    service_message = {
        "role": "system", 
        "content": f"""
        Available Services related to the latest query:
        {services_text}
        
        Based on the user's request and the available services, provide a recommendation on which Razorpay internal services to use.
        Include:
        1. The recommended service(s)
        2. A brief explanation of why these services are appropriate
        3. A simple example of how to use these services for the requested task
        """
    }
    messages.append(service_message)
    
    # Call OpenAI API with the enhanced messages
    response = await client.chat.completions.create(
        messages=messages,
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        stream=True
    )
    
    # Generate filename based on timestamp and query
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    query_slug = query.lower().replace(" ", "_")[:30]  # First 30 chars of query as slug
    filename = f"{timestamp}_{query_slug}.txt"
    file_path = recommendations_dir / filename
    
    # Stream the response and save to file
    print("### Service Recommendation Agent :>\n", end="", flush=True)
    full_response = ""
    
    # Create the file and write the query
    with open(file_path, "w") as f:
        f.write(f"Query: {query}\n\n")
        f.write("Recommendation:\n")
    
    async for chunk in response:
        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
            
            # Append to file
            with open(file_path, "a") as f:
                f.write(content)
    
    # Add assistant response to conversation history
    history.append({"role": "assistant", "content": full_response})
    
    print(f"\n\nRecommendation saved to: {file_path}")
    return full_response

    history.append({"role": "user", "content": query})

    # Search for services
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    services_info = []
    if 'documents' in results and results['documents']:
        documents = results['documents']
        print(f"Documents structure: {len(documents)} lists with {[len(d) for d in documents]} items")
        
        for doc_list in documents:
            if doc_list:  # Check if the list is not empty
                for doc in doc_list:
                    services_info.append(doc)
    
    if not services_info:
        print("No matching services found for your query")
        return "No matching services found."
    
    services_text = "\n\n".join(services_info)

    messages = history.copy()
    
    # Create prompt with available services info
    prompt = f"""
    User Request: {query}
    
    Available Services:
    {services_text}
    
    Based on the user's request and the available services, provide a recommendation on which Razorpay internal services to use.
    Include:
    1. The recommended service(s)
    2. A brief explanation of why these services are appropriate
    3. A simple example of how to use these services for the requested task
    """
    
    # Add user query to conversation history
    history.append({"role": "user", "content": prompt})
    
    # Call OpenAI API with the full conversation history
    response = await client.chat.completions.create(
        messages=history,
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        stream=True
    )
    
    # Generate filename based on timestamp and query
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    query_slug = query.lower().replace(" ", "_")[:30]  # First 30 chars of query as slug
    filename = f"{timestamp}_{query_slug}.txt"
    file_path = recommendations_dir / filename
    
    # Stream the response and save to file
    print("### Service Recommendation Agent :>\n", end="", flush=True)
    full_response = ""
    
    # Create the file and write the query
    with open(file_path, "w") as f:
        f.write(f"Query: {query}\n\n")
        f.write("Recommendation:\n")
    
    async for chunk in response:
        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
            
            # Append to file
            with open(file_path, "a") as f:
                f.write(content)
    
    # Add assistant response to conversation history
    history.append({"role": "assistant", "content": full_response})
    
    print(f"\n\nRecommendation saved to: {file_path}")
    return full_response

async def main():
    global conversation_history
    
    print("Welcome to the Razorpay Service Recommender")
    print("===========================================")
    print("Type 'exit' to quit the application")
    print("Type 'new' to start a new conversation")
    
    while True:
        user_input = input("\nDescribe what you need to accomplish: ")
        
        if user_input.lower() == 'exit':
            print("Thank you for using the Service Recommender. Goodbye!")
            break
        
        if user_input.lower() == 'new':
            conversation_history = [
                {"role": "system", "content": "You are a Razorpay internal service recommendation agent. Your task is to help employees find the right internal services for their tasks. Maintain context from previous messages in the conversation."}
            ]
            print("Started a new conversation!")
            continue
        
        try:
            await get_service_recommendations(user_input, conversation_history)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
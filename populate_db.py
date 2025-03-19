import os
import json
import chromadb
from dotenv import load_dotenv

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Error loading .env file: {e}")

# Initialize Chroma client
client = chromadb.PersistentClient(path="./chroma_db")

# Check if collection exists, if it does, delete it to start fresh
try:
    client.delete_collection("razorpay_services")
    print("Deleted existing collection")
except:
    print("No existing collection to delete")

# Create a collection for services
collection = client.create_collection(name="razorpay_services")

# Path to the folder containing the chunked files
chunked_files_dir = "./chunked_files"

# Prepare the data for Chroma (same as your existing setup)
ids = []
documents = []
metadatas = []

# Function to process each chunk file and add it to the database
def process_chunk_file(file_path):
    try:
        with open(file_path, "r") as file:
            chunks = json.load(file)

            for chunk in chunks:
                # Extract the necessary fields from the chunk
                chunk_id = chunk.get("id")
                name = chunk.get("name")
                description = chunk.get("description", "")
                use_cases = "\n".join(chunk.get("use_cases", []))
                capabilities = "\n".join(chunk.get("capabilities", []))
                references = "\n".join(chunk.get("references", []))

                # Prepare the document as a formatted string
                document = (
                    f"Name: {name}\n"
                    f"Description: {description}\n"
                    f"Use Cases: {use_cases}\n"
                    f"Capabilities: {capabilities}\n"
                    f"References: {references}"
                )

                # Prepare metadata as a dictionary
                metadata = {
                    "name": name,
                    "capabilities": capabilities,
                    "references": references
                }

                # Prepare data for adding to the database
                ids.append(chunk_id)
                documents.append(document)
                metadatas.append(metadata)
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Iterate through all the files in the chunked_files directory
for filename in os.listdir(chunked_files_dir):
    file_path = os.path.join(chunked_files_dir, filename)
    
    if file_path.endswith(".json"):  # Process only JSON files
        print(f"Processing {file_path}...")
        process_chunk_file(file_path)

# Add all the chunks to the collection in Chroma
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print(f"Added {len(ids)} chunks to the database.")

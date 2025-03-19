import chromadb
import os
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

# Define your internal services with descriptions
services = [
    {
        "id": "beam-service",
        "name": "Beam Service",
        "description": "A service that fetches files from SFTP servers. It can connect to external SFTP locations, authenticate, and download files in various formats.",
        "use_cases": "File transfer from external partners, fetching data from SFTP servers, automating file downloads",
        "capabilities": "SFTP connection, file download, scheduling, authentication"
    },
    {
        "id": "batch-service",
        "name": "Batch Service",
        "description": "A service that uploads files to Amazon S3 buckets and performs various operations on them. It handles large file uploads efficiently.",
        "use_cases": "Storing files in S3, processing large batches of data, data archiving",
        "capabilities": "S3 upload, file processing, batch operations, compression"
    },
    {
        "id": "payment-processor",
        "name": "Payment Processor",
        "description": "Core payment processing service that handles transactions across multiple payment methods.",
        "use_cases": "Processing payments, refunds, and settlements",
        "capabilities": "Multiple payment gateways, fraud detection, international payments"
    },
    {
        "id": "notification-service",
        "name": "Notification Service",
        "description": "Service for sending notifications via email, SMS, and push notifications.",
        "use_cases": "Transaction alerts, OTP delivery, marketing campaigns",
        "capabilities": "Multi-channel notifications, templating, scheduling"
    },
    {
        "id": "analytics-engine",
        "name": "Analytics Engine",
        "description": "Service for processing and analyzing transaction and user data.",
        "use_cases": "Business intelligence, user behavior analysis, fraud detection",
        "capabilities": "Real-time analytics, reporting, dashboard integration"
    },
    {
        "id": "api-gateway",
        "name": "API Gateway",
        "description": "Central API management service that handles routing, authentication, and rate limiting.",
        "use_cases": "API management, microservice communication, external API integration",
        "capabilities": "Routing, authentication, rate limiting, API versioning"
    },
    {
        "id": "data-pipeline",
        "name": "Data Pipeline",
        "description": "Service for building ETL pipelines to transform and process data across systems.",
        "use_cases": "Data transformation, ETL processes, real-time data processing",
        "capabilities": "Stream processing, batch processing, data transformation"
    },
    {
        "id": "document-processor",
        "name": "Document Processor",
        "description": "Service for parsing, validating, and processing structured documents.",
        "use_cases": "KYC document verification, invoice processing, contract analysis",
        "capabilities": "OCR, document validation, information extraction"
    }
]

# Prepare data for Chroma
ids = [service["id"] for service in services]
documents = [
    f"Name: {service['name']}\nDescription: {service['description']}\nUse Cases: {service['use_cases']}\nCapabilities: {service['capabilities']}"
    for service in services
]
metadatas = [
    {
        "name": service["name"],
        "capabilities": service["capabilities"]
    } for service in services
]

# Add data to the collection
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

print(f"Added {len(services)} services to the database")
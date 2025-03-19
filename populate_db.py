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
        "capabilities": "SFTP connection, file download, scheduling, authentication",
        "references": ["https://example.com/beam-service-docs"]
    },
    {
        "id": "batch-service",
        "name": "Batch Service",
        "description": "A service that uploads files to Amazon S3 buckets and performs various operations on them. It handles large file uploads efficiently.",
        "use_cases": "Storing files in S3, processing large batches of data, data archiving",
        "capabilities": "S3 upload, file processing, batch operations, compression",
        "references": ["https://example.com/batch-service-docs"]
    },
    {
        "id": "payment-processor",
        "name": "Payment Processor",
        "description": "Core payment processing service that handles transactions across multiple payment methods.",
        "use_cases": "Processing payments, refunds, and settlements",
        "capabilities": "Multiple payment gateways, fraud detection, international payments",
        "references": ["https://example.com/payment-processor-docs"]
    },
    {
        "id": "notification-service",
        "name": "Notification Service",
        "description": "Service for sending notifications via email, SMS, and push notifications.",
        "use_cases": "Transaction alerts, OTP delivery, marketing campaigns",
        "capabilities": "Multi-channel notifications, templating, scheduling",
        "references": ["https://example.com/notification-service-docs"]
    },
    {
        "id": "analytics-engine",
        "name": "Analytics Engine",
        "description": "Service for processing and analyzing transaction and user data.",
        "use_cases": "Business intelligence, user behavior analysis, fraud detection",
        "capabilities": "Real-time analytics, reporting, dashboard integration",
        "references": ["https://example.com/analytics-engine-docs"]
    },
    {
        "id": "api-gateway",
        "name": "API Gateway",
        "description": "Central API management service that handles routing, authentication, and rate limiting.",
        "use_cases": "API management, microservice communication, external API integration",
        "capabilities": "Routing, authentication, rate limiting, API versioning",
        "references": ["https://example.com/api-gateway-docs"]
    },
    {
        "id": "data-pipeline",
        "name": "Data Pipeline",
        "description": "Service for building ETL pipelines to transform and process data across systems.",
        "use_cases": "Data transformation, ETL processes, real-time data processing",
        "capabilities": "Stream processing, batch processing, data transformation",
        "references": ["https://example.com/data-pipeline-docs"]
    },
    {
        "id": "document-processor",
        "name": "Document Processor",
        "description": "Service for parsing, validating, and processing structured documents.",
        "use_cases": "KYC document verification, invoice processing, contract analysis",
        "capabilities": "OCR, document validation, information extraction",
        "references": ["https://example.com/document-processor-docs"]
    }
]

spinnaker_steps = [
    {
        "id": "create-service-account",
        "name": "Create Service Account",
        "description": "Create a service account with the necessary cluster role and role binding to allow Spinnaker to access the new cluster.",
        "commands": [
            "kubectl get sa -n spinnaker spinnaker",
            "kubectl create sa spinnaker -n spinnaker",
            "kubectl create clusterrolebinding spinnaker-admin --clusterrole=cluster-admin --serviceaccount=spinnaker:spinnaker"
        ],
        "use_cases": "Grant Spinnaker access to the new cluster",
        "dependencies": "Kubernetes cluster, appropriate permissions",
        "references": ["https://example.com/create-service-account-docs"]
    },
    {
        "id": "store-tokens",
        "name": "Store Tokens in Credstash",
        "description": "Store the generated service account tokens securely in Credstash for authentication.",
        "commands": [
            "credstash put credstash-prod-ops <generated-token>"
        ],
        "use_cases": "Secure authentication for Spinnaker",
        "dependencies": "Credstash access",
        "references": ["https://example.com/store-tokens-docs"]
    },
    {
        "id": "update-vishnu-config",
        "name": "Update Vishnu Config",
        "description": "Modify Vishnu configuration files to include the new cluster credentials.",
        "commands": [
            "Update vishnu/modules/applications/spinnaker/templates/kubeconfig.tpl",
            "Update vishnu/modules/applications/spinnaker/templates/halconfig.tpl"
        ],
        "use_cases": "Ensure Spinnaker can use the new cluster",
        "dependencies": "Vishnu repository access",
        "references": ["https://example.com/update-vishnu-config-docs"]
    },
    {
        "id": "update-hal-pod",
        "name": "Update Halyard Configuration",
        "description": "Modify Halyard pod configurations and copy required files.",
        "commands": [
            "kubectl exec -it deploy/halyard -n <spinnaker-namespace> -- /bin/bash",
            "mkdir -p /home/spinnaker/.hal/default/service-settings/",
            "mkdir -p /home/spinnaker/.kube/",
            "mkdir -p /home/spinnaker/.ssh/",
            "mkdir -p /home/spinnaker/.hal/default/profiles/",
            "cp /home/spinnaker/halconfig/* /home/spinnaker/.hal/default/profiles/",
            "cp /home/spinnaker/halconfig/kubeconfig /home/spinnaker/.kube/config"
        ],
        "use_cases": "Prepare Halyard for the new cluster",
        "dependencies": "Halyard pod access",
        "references": ["https://example.com/update-hal-pod-docs"]
    },
    {
        "id": "apply-config",
        "name": "Apply Configuration",
        "description": "Apply the new configuration to Spinnaker and verify cluster connectivity.",
        "commands": [
            "hal config",
            "kubectl config use-context <cluster-name>",
            "kubectl get pods -A",
            "hal deploy apply --delete-orphaned-services"
        ],
        "use_cases": "Deploy the new cluster configuration",
        "dependencies": "Spinnaker CLI (hal)",
        "references": ["https://example.com/apply-config-docs"]
    },
    {
        "id": "verify-deployment",
        "name": "Verify Deployment",
        "description": "Ensure all Spinnaker pods are running properly and test a deployment.",
        "commands": [
            "kubectl -n <spinnaker-namespace> get po",
            "Trigger a test deployment from the Spinnaker console"
        ],
        "use_cases": "Ensure Spinnaker is functioning correctly with the new cluster",
        "dependencies": "Spinnaker UI access",
        "references": ["https://example.com/verify-deployment-docs"]
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
        "capabilities": service["capabilities"],
        "references": ", ".join(service["references"])
    } for service in services
]

# Add data to the collection
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)

# Prepare data for Chroma
spinnaker_ids = [step["id"] for step in spinnaker_steps]
spinnaker_documents = [
    f"Name: {step['name']}\nDescription: {step['description']}\nCommands: {' | '.join(step['commands'])}\nUse Cases: {step['use_cases']}\nDependencies: {step['dependencies']}"
    for step in spinnaker_steps
]


spinnaker_metadatas = [
    {
        "name": step["name"],
        "dependencies": step["dependencies"],
        "references": ", ".join(step["references"])
    } for step in spinnaker_steps
]

# Add data to the collection
collection.add(
    ids=spinnaker_ids,
    documents=spinnaker_documents,
    metadatas=spinnaker_metadatas
)

# Print confirmation
print("Data added to the collection.")

print(f"Added {len(services)} services to the database")
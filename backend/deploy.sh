#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
BACKEND_SERVICE="chat-security-backend"
FRONTEND_SERVICE="chat-security-frontend"

echo "Using Project: $PROJECT_ID"
echo "Region: $REGION"

# 1. Create Secret (if not exists)
echo "--- Configuring Secrets ---"
if ! gcloud secrets describe gemini-api-key &>/dev/null; then
    echo "Creating gemini-api-key secret..."
    read -sp "Enter your Gemini API Key: " GEMINI_KEY
    echo
    printf "%s" "$GEMINI_KEY" | gcloud secrets create gemini-api-key --data-file=-
else
    echo "Secret gemini-api-key already exists. Skipping creation."
fi

# 2. Deploy Backend
echo "--- Deploying Backend ---"
gcloud run deploy $BACKEND_SERVICE \
    --source . \
    --platform managed \
    --region $REGION \
    --port 8080 \
    --allow-unauthenticated \
    --set-secrets="GOOGLE_API_KEY=gemini-api-key:latest"

# Get Backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --platform managed --region $REGION --format 'value(status.url)')
echo "Backend deployed at: $BACKEND_URL"

# 3. Deploy Frontend
echo "--- Deploying Frontend ---"
# We need to build the container first to pass build-args, 
# or use Cloud Build. Using 'gcloud run deploy --source' uses Cloud Build automatically.
# But passing build-args to 'gcloud run deploy --source' isn't directly supported in a simple flag sometimes.
# Let's use gcloud builds submit then deploy to be safe and explicit about build-args.

echo "Building Frontend Container image..."
gcloud builds submit frontend/ \
    --tag gcr.io/$PROJECT_ID/$FRONTEND_SERVICE \
    --substitutions=_NEXT_PUBLIC_API_URL=$BACKEND_URL

echo "Deploying Frontend Service..."
gcloud run deploy $FRONTEND_SERVICE \
    --image gcr.io/$PROJECT_ID/$FRONTEND_SERVICE \
    --platform managed \
    --region $REGION \
    --port 8080 \
    --allow-unauthenticated

# Get Frontend URL
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --platform managed --region $REGION --format 'value(status.url)')

echo "--- Deployment Complete ---"
echo "Backend: $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"

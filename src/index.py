from flask import Flask, jsonify, request
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
import os

# Import env vars
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WEAVIATE_CLUSTER_API_KEY = os.environ.get('WEAVIATE_CLUSTER_API_KEY')
WEAVIATE_CLUSTER_URL="https://question-finder-alpha-doxx6cid.weaviate.network"

if not OPENAI_API_KEY or not WEAVIATE_CLUSTER_API_KEY:
    raise ValueError("API keys are not set in environment variables")

# Serializer for query result, because Document type is not JSON serializable. Document has a property called page_content which is what we want returned
def serialize_document(document):
    # Assuming 'document' has attributes that you want to include in the JSON
    return {
        'surveyQuestion': document.page_content,
    }
app = Flask(__name__)

client = weaviate.Client(
    url=WEAVIATE_CLUSTER_URL,  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_CLUSTER_API_KEY),  # Replace w/ your Weaviate instance API key
)
# Initialize vectorsotre
vectorstore = Weaviate(
    client=client, 
    index_name="SurveyQuestions", 
    text_key="text", 
    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY), 
    by_text=False
)
print('Connected to weaviate...')

@app.route('/search', methods=['GET'])
def get_incomes():
    args = request.args
    query = args.get("query", default=None, type=str)

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        results = vectorstore.similarity_search(query)
        serialized_results = [serialize_document(doc) for doc in results]
        return jsonify(serialized_results)
    except Exception as e:
        # Handle exceptions such as network issues
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



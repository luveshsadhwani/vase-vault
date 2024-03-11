from flask import Flask, jsonify, request
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
import os
import functools

# Import env vars
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WEAVIATE_CLUSTER_API_KEY = os.environ.get('WEAVIATE_CLUSTER_API_KEY')
WEAVIATE_CLUSTER_URL=os.environ.get('WEAVIATE_CLUSTER_URL')
API_KEY = os.environ.get('API_KEY')

if not OPENAI_API_KEY or not WEAVIATE_CLUSTER_API_KEY:
    raise ValueError("API keys are not set in environment variables")

# Serializer for query result, because Document type is not JSON serializable. Document has a property called page_content which is what we want returned
def serialize_document(document):
    #   Sample document: 
    #   Document(
    #       page_content='Question: Are you currently using a 5G mobile line?\nAnswer Choices: YES; NO; Not sure\n: ', 
    #       metadata={
    #           'linkToIvery': 'https://admin.askevery.com/survey/###', 
    #           'organizationName': '###', 
    #           'questionNumber': 'Q6', 
    #           'questionType': 'MC', 
    #           'surveyCompletionDate': '####-##-## 14:54:15', 
    #           'surveyName': '#### ## ######'
    #          }
    #   )
    return {
        'surveyQuestion': document.page_content,
        'linkToIvery': document.metadata["linkToIvery"], # properties are in a dict., so use bracket notation
        'organizationName': document.metadata["organizationName"], 
        'questionNumber': document.metadata["questionNumber"], 
        'questionType': document.metadata["questionType"], 
        'surveyCompletionDate': document.metadata["surveyCompletionDate"], 
        'surveyName': document.metadata["surveyName"], 
    }
app = Flask(__name__)

def require_api_key(view_function):
    @functools.wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('API-KEY')
        if api_key and api_key == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({"message": "Access denied"}), 401
    return decorated_function

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
    by_text=False,
    attributes=["surveyName", "questionNumber","questionType","surveyName","linkToIvery","organizationName","surveyCompletionDate"]
)
print('Connected to weaviate...')

@app.route('/search', methods=['GET'])
@require_api_key
def search_vase_vault():
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



# Script to vector search for questions 

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WEAVIATE_CLUSTER_API_KEY = os.environ.get('WEAVIATE_CLUSTER_API_KEY')
WEAVIATE_CLUSTER_URL="https://question-finder-alpha-doxx6cid.weaviate.network"

if not OPENAI_API_KEY or not WEAVIATE_CLUSTER_API_KEY:
    raise ValueError("API keys are not set in environment variables")

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

query="Mobile users with 5G"
result = vectorstore.similarity_search(query)
print(result)
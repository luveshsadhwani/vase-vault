# Script specifically for loading embedded data from csv into weaviate database

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WEAVIATE_CLUSTER_API_KEY = os.environ.get('WEAVIATE_CLUSTER_API_KEY')
WEAVIATE_CLUSTER_URL=os.environ.get('WEAVIATE_CLUSTER_URL')

if not OPENAI_API_KEY or not WEAVIATE_CLUSTER_API_KEY:
    raise ValueError("API keys are not set in environment variables")

# Split data into what needs to be embedded and metadata
loader = CSVLoader(
    file_path="./scripts/vase_vault_full.csv",
    metadata_columns=["questionNumber","questionType", "linkToIvery","organizationName","surveyCompletionDate", "surveyName"]
)

data = loader.load()

client = weaviate.Client(
    url=WEAVIATE_CLUSTER_URL,  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_CLUSTER_API_KEY),  # Replace w/ your Weaviate instance API key
)

print("ADDING TO WEAVIATE")
vectorstore = Weaviate.from_documents(
    client = client,
    documents = data,
    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY),
    index_name="SurveyQuestions",
    text_key="text"
)
print("LOADING EMBEDDED SURVEY QUESTIONS COMPLETE")
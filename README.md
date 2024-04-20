## API Development

1. Create start up file named `bootstrap.sh`. This file initializes the environment for the API development.
2. export env variables

-   In bootstrap.sh, export the following environment variables:
    -   `FLASK_APP`: Path to your Flask application entry point. Example: `export FLASK_APP=./src/index.py`.
    -   `OPENAI_API_KEY`: Your OpenAI API key, used for accessing OpenAI embeddings. Example: `export OPENAI_API_KEY="your_openai_api_key"`.
    -   `WEAVIATE_CLUSTER_API_KEY`: Your Weaviate cluster API key, used for accessing the vectorstore. Example: `export WEAVIATE_CLUSTER_API_KEY="your_weaviate_cluster_api_key"`.
    -   `API_KEY`: Secure API key for authentication

3. Make bootstrap.sh executable using `chmod +x bootstrap.sh`
4. Running the API:

-   Execute the bootstrap.sh script to set up the environment and run your Flask application.

## Deployment via Fly

1. Install gunicorn to serve the app
2. Save all dependencies, `pip3 freeze > requirements.txt`
3. Configure and launch the app using `fly launch`
4. Modify profile to use the correct starting point `src.index:app`
5. Set env files - `OPENAI_API_KEY`, `WEAVIATE_CLUSTER_API_KEY`,`API_KEY`

## Scripts

1. Create a `.env` file based off of `.env.example`
2. Add relevant env variables

-   `OPENAI_API_KEY` for access to openai embeddings
-   `WEAVIATE_CLUSTER_API_KEY` for access to the vectorstore
-   `WEAVIATE_CLUSTER_URL`

3. Run script with `python3 <SCRIPT_NAME>`

## Updating vase vault - create new instance

1. Create new weaviate instance
2. Download latest questions from vase vault on google drive
3. Update `vase_vault_full.csv` with latest questions and format the header row
4. Update new `WEAVIATE_CLUSTER_API_KEY` and `WEAVIATE_CLUSTER_URL`
5. Run `load_data` script
6. Deploy`vase_vault` backend with new fly secrets

## Updating vase vault - extend current instance

1. Extend current weaviate instance in dashboard
2. Download new survey questions from previous update
3. Update `vase_vault_full.csv` with latest questions and format the header row
4. Run `load_data` script

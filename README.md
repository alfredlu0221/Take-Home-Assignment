## Project description
This project provides financial API services in Python for development purposes.

## Tech stack
    - Programming languages (Python)
    - Frameworks (Flask, Docker)
    - Databases (SQLite)
    - Command line tools (Curl, Git Bash)

## How to run the code in local environment
1. To start docker application and to confirm that it is running properly, run the following command:
```bash
 docker compose -f docker-compose.yml up --build
```
2. Open a new terminal then make a GET request to the server using the curl commands:

Get financial data API:
```bash
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-05-01&end_date=2023-05-31&symbol=IBM&limit=3&page=2'
```

Get statistics API:
```bash
curl -X GET 'http://localhost:5000/api/statistics?start_date=2023-05-01&end_date=2023-05-31&symbol=IBM'
```

## How to maintain the API key to retrieve financial data from AlphaVantage in both local development and production environment.
### Local development:
1. Store them in a .env file.
2. Don’t commit them to a code repository.

### Production environment
1. Added all API keys and/or secrets as environment variables, It will be able to easily manage them.
2. Should not embed API keys directly in code.
3. Should not store API keys in files inside the application's source tree.
4. Restrict the API keys to be used by only the IP addresses, referrer URLs, and mobile apps that need them.
5. Restrict the API keys to be usable only for certain APIs.
6. Delete unneeded API keys.
7. Rotate the API keys periodically.

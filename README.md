# AI Chat Bot for Protracking App

This chat bot is designed to be utilized within the Protracking App.

This application is developed using FastAPI, Langchain, and OpenAI.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

Use uvicorn to run the app.

```bash
uvicorn main:app --reload
```

## Features

- [x] User Authentication
- [x] Chat Bot + Google Search

## API Documentation

The API documentation is available at `/docs`.

## Configuration

Create a .env file in the root directory of the project and add the following variables.

```bash
OPENAI_API_KEY=YOUR_API_KEY

GOOGLE_CSE_ID=YOUR_CSE_ID
GOOGLE_API_KEY=YOUR_API_KEY

DB_URL=YOUR_DB_URL

ALLOWED_ORIGINS=YOUR_ALLOWED_ORIGINS

# This is config to connect with the Protracking App
JWT_SECRET=YOUR_JWT_SECRET
JWT_ALGORITHM=YOUR_JWT_ALGORITHM
JWT_EXPIRE_TIME=YOUR_JWT_EXPIRE_TIME

EXTERNAL_SERVER_URL=YOUR_EXTERNAL_SERVER_URL
EXTERNAL_SERVER_ISS=YOUR_EXTERNAL_SERVER_ISS
EXTERNAL_SERVER_AUD=YOUR_EXTERNAL_SERVER_AUD
EXTERNAL_SERVER_NAME=YOUR_EXTERNAL_SERVER_NAME
EXTERNAL_SERVER_EMAIL=YOUR_EXTERNAL_SERVER_EMAIL
EXTERNAL_SERVER_PASSWORD=YOUR_EXTERNAL_SERVER_PASSWORD
EXTERNAL_SERVER_ACCOUNT_TYPE=YOUR_EXTERNAL_SERVER_ACCOUNT_TYPE
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

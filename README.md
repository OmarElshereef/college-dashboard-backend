# college management with mini rag

This is a minimal implementation of the RAG (Retrieval-Augmented Generation) model for question answering.

## Requirements

- Python 3.13 or later
- A virtual environment (recommended)

## Setup

### 1. Create and activate a virtual environment

```bash
$ python3.13 -m venv venv
$ source venv/bin/activate    # On Linux/Mac
$ venv\Scripts\activate       # On Windows
```

### 2. Install the required packages

```bash
$ pip install -r requirements.txt
```

### 3. Setup the environment variables

```bash
$ cp .env.example .env
```

Edit the `.env` file and set your environment variables (e.g., `OPENAI_API_KEY`).

## Run the FastAPI server

```bash
$ uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

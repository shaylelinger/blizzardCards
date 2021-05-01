# Blizzard Home Assignment: 1. Software Engineering

## Description

In this exercise, we are creating an app which reads API card data and renders a card list according to specifications.

We'll be using Python 3 and Flask for the web app.

There's also a CLI version of the app for quick testing (cardsCLI.py).

The design is very straightforward:

1. Load credentials from .env file (in production secrets would be stored in a more secure location)
2. Use credentials to get access token
3. Fetch card data
4. Fetch metadata
5. Join card data and metadata and create output object
6. Render HTML

## Getting Started

### Dependencies

##### For CLI:
Python 3
requests package
Run command:
``` 
pip3 install requests
```

#### For Flask app:
Run command:
```
pip3 install -r requirements.txt
```

##### For container:
Ensure Docker is installed, Dockerfile will take care of the rest

### Executing program

##### CLI:
Get API access token manually and store in env variable:
```
export BLIZZARD_TEMP_API_ACCESS_TOKEN='someKindOfToken'
```
Run command:
```
./cardsCLI.py
```

##### Web app:
1. Store client ID, client secret and card limit in .env file inside /app folder:
```
BLIZZARD_API_CLIENT_ID='someClientId'
BLIZZARD_API_CLIENT_SECRET='someClientSecret'
BLIZZARD_CARD_LIMIT=10
```

2. Build Docker image
```
docker build -t blizzcards:latest .
```
3. Run Docker container
```
docker run --name blizzcards -v$PWD/app:/app -p8080:8080 blizzcards:latest&
```
4. Go to http://localhost:8080

#!/usr/local/bin/python3

import json
from flask import Flask, Response, render_template, abort
import os
import requests
from dotenv import load_dotenv

# locate metadata name by id
def getCardMetadata(lookupData, lookupId):
	try:
		for item in lookupData:
			if item['id'] == lookupId:
				return item['name']
	except Exception as e:
		abort(500, description=f'Error looking up card metadata: {e}')	

	return None

# get oauth access token
def getAccessToken():
	ACCESS_TOKEN_URL = 'https://us.battle.net/oauth/token'
	
	params = {'grant_type': 'client_credentials'}

	try:
		client_id = os.getenv('BLIZZARD_API_CLIENT_ID')
		client_secret = os.getenv('BLIZZARD_API_CLIENT_SECRET')

		response = requests.post(ACCESS_TOKEN_URL, auth=(client_id, client_secret), data=params)
		return response.json()['access_token']
	except Exception as e:
		abort(500, description=f'Error getting access token: {e}')


# fetch data from api endpoints and call processData
def getData():
	accessToken = getAccessToken()

	# API data URLs
	CARDS_URL = f'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&class=druid%2Cwarlock&manaCost=7%2C8%2C9%2C10&rarity=legendary&sort=id%3Aasc&access_token={accessToken}'
	METADATA_URL = f'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token={accessToken}'

	try:
		# get data
		response = requests.get(CARDS_URL)
		cardData = response.json()
	except Exception as e:
		abort(500, description=f'Error getting card data: {e}')	

	try:
		response = requests.get(METADATA_URL)
		metadata = response.json()
	except Exception as e:
		abort(500, description=f'Error getting metadata: {e}')	

	return processData(cardData, metadata)

# process data and return output list for visualization
def processData(cardData, metadata):
	# init output array
	output = []

	# populate output objects array with card data + metadata
	for card in cardData['cards']:
		outputObject = {}

		outputObject['image'] = card['image']
		outputObject['name'] =  card['name']

		outputObject['cardType'] = getCardMetadata(metadata['types'], card['cardTypeId'])
		outputObject['rarity'] = getCardMetadata(metadata['rarities'], card['rarityId'])
		outputObject['cardSet'] = getCardMetadata(metadata['sets'], card['cardSetId'])
		outputObject['class'] = getCardMetadata(metadata['classes'], card['classId'])
		
		output.append(outputObject)

	return output

# initialize flask
app = Flask(__name__)

@app.route("/")
def index():
	# load env variables from .env file
	load_dotenv()

	# render html template using output data
	return render_template('index.html', output=getData())

# run app
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)
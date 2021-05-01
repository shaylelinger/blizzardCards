#!/usr/bin/env python3

import json
from flask import Flask, Response, render_template
import os
import requests

def getCardMetadata(lookupData, lookupId):
	for item in lookupData:
		if item['id'] == lookupId:
			return item['name']

	return None

def getAccessToken(clientId, clientSecret):
	return

# initialize flask
app = Flask(__name__)

@app.route("/")
def index():
	# add oauth flow
	access_token = os.environ['BLIZZARD_TEMP_API_ACCESS_TOKEN']

	# API data URLs
	CARDS_URL = f'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&class=druid%2Cwarlock&manaCost=7%2C8%2C9%2C10&rarity=legendary&sort=id%3Aasc&access_token={access_token}'
	METADATA_URL = f'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token={access_token}'

	# get data
	response = requests.get(CARDS_URL)
	cardData = response.json()

	response = requests.get(METADATA_URL)
	metadata = response.json()

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
	
	return render_template('index.html', output=output)

# run app
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)
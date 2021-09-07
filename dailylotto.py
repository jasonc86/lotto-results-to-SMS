#!/usr/bin/python3
'''Module for retrieving the NY lottery numbers and Win 4 game results'''
import time
import json
import requests
from random_ua import rand_user_agent

def request_json(game):
	'''Request for JSON data from url.'''
	url = f'https://nylottery.ny.gov/nyl-api/games/{game}/draws'
	headers = {'User-agent': rand_user_agent()}
	try:
		res = requests.get(url, headers=headers, timeout=60)
		res.raise_for_status()
	except requests.HTTPError as e:
		print(f'Status Code: {e.response.status_code}')
		return False
	return res.text

def result_check(game):
	'''Checks JSON data to see if results are available for latest game.
	   if "results" key in draw_data exists it returns draw_data.'''
	json_data = request_json(game)
	if json_data:
		draw_data = json.loads(json_data)['data']['draws'][1]
		if draw_data.get('results', ''):
			return draw_data

def json_to_str(draw_data):
	'''Converts JSON data to string and formats it for readability.
	   See included JSON files to see how the desired data is structured.'''
	results = draw_data.get('results', '')
	draw_period = {1: "Midday", 2: "Evening"}
	numbers = ''.join(results[0]['primary'])
	result_date = time.strftime("%x", time.localtime((draw_data['resultDate']/1000)))
	url = f"https://nylottery.ny.gov/draw-game?game={draw_data['gameName']}"
	timestamp = f"Retrieved at {time.strftime('%X')} from\n{url}"
	results_info = (draw_period[draw_data['drawPeriod']],
		draw_data['gameName'].title(), result_date, numbers, timestamp)
	return "{0[0]} {0[1]} ({0[2]}): {0[3]}\n{0[4]}".format(results_info)

def format_sms(games):
	'''Records draw data for each game and combines it into one string to send via SMS.'''
	while not all([v for v in games.values()]):
		for game in games.keys():
			draw_data = result_check(game) 
			if draw_data and not games[game]:
				games[game] = json_to_str(draw_data)
				continue
			time.sleep(30)
	return '\n\n'.join([v for v in games.values()])

def main():
	games = {'numbers':False, 'win4':False}
	print(format_sms(games))

if __name__ == '__main__':
	main()

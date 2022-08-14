#!/usr/bin/python3
'''Module for retrieving the NY lottery numbers and Win 4 game results'''
import time
import requests
import sys
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
	return res.json()

def result_check(game):
	'''Checks JSON data to see if results are available for latest game.
	   if "results" key in draw_data exists it returns draw_data.'''
	json_data = request_json(game)
	if json_data:
		draw_data = json_data['data']['draws'][1]
		if draw_data.get('results', ''):
			return draw_data
	else:
		return False

def json_to_str(draw_data):
	'''Converts JSON data to string and formats it for readability.
	   See included JSON files to see how the desired data is structured.'''
	try:
		results = draw_data.get('results', '')
	except AttributeError:
		return False
	draw_period = {1: "Midday", 2: "Evening"}
	numbers = ''.join(results[0]['primary'])
	result_date = time.strftime("%x", time.localtime((draw_data['resultDate']/1000)))
	results_info = (draw_period[draw_data['drawPeriod']],
		draw_data['gameName'].title(), result_date, numbers)
	return "{0[1]}: {0[3]}".format(results_info), "{0[0]} {0[2]}".format(results_info)

def format_sms(games, interval, timeout):
	'''Checks to see if results for each game is available. If it isn't it waits and then checks the results for the other game.'''
	start = time.time()
	while not all([v for v in games.values()]):
		for game in games.keys():
			draw_data = result_check(game)
			if draw_data and not games[game]:
				games[game] = json_to_str(draw_data)
			else:
				time.sleep(interval)
		if time.time() - start > timeout:
			for k, v in games.items():
				url = f"https://nylottery.ny.gov/draw-game?game={k}."
				if v == False:
					games[k] = f"Request failed. Retrieve results at {url}"
			break

def main():
	games = {'numbers':False, 'win4':False}
	format_sms(games, 30, 3600)
	print('\n'.join([v[0] for v in games.values()]+[v[1] for v in games.values()][1:]))
	#print([v for v in games.values()])

if __name__ == '__main__':
	main()

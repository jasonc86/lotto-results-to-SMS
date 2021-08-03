#!/usr/bin/python3
'''Module for texting myself the NY lottery numbers and Win 4 game results'''
import time
import json
import requests
from random_ua import rand_user_agent
from twtxt import twilio_text

def request_json(game):
	'''Request for JSON data. Request is made ten times in case of temporary connection issues.
	   After the tenth request, the program just sends a link to the NY lottery website.
	   If my computer can't connect and send anything out,
	   I can still use the links provided in previous messages.'''
	url = f'https://nylottery.ny.gov/nyl-api/games/{game}/draws'
	headers = {'User-agent': rand_user_agent()}
	for _ in range(10):
		try:
			res = requests.get(url, headers=headers, timeout=60)
			res.raise_for_status()
			break
		except requests.HTTPError as e:
			print(f"{_}...")
			print(f"status code: {res.status_code}")
			time.sleep(.5)
			err = str(e)
			continue
	else:
		raise Exception(f"Request failed for {game.title()}.\n{err}")
	return json.loads(res.text)['data']['draws'][1]

def result_check(draw_data):
	'''Checks JSON data to see if results are available for latest game.
	   if "results" key in draw_data exists it returns True, otherwise it returns False.'''
	return draw_data.get('results', '')

def json_to_str(draw_data, game):
	'''Converts JSON data to formatted string to send to my phone as a text message.
	   See included JSON files to see how the desired data is structured.'''
	results = draw_data.get('results', '')
	draw_period = {1: "Midday", 2: "Evening"}
	numbers = ''.join(results[0]['primary'])
	result_date = time.strftime("%m/%d/%y", time.localtime((draw_data['resultDate']/1000)))
	results_info = (draw_period[draw_data['drawPeriod']],
		game.title(), result_date, numbers)
	return "{0[0]} {0[1]} ({0[2]}): {0[3]}".format(results_info)

def timestamp():
	'''Adds a timestamp at the end of the message with a link to the results 
	to double check.'''
	url = "https://nylottery.ny.gov/draw-game?game="
	games = ['numbers', 'win4']
	ts = time.strftime('%-I:%M%p')
	return "Retrieved at {0} from\n{1}{2[0]}\n{1}{2[1]}.".format(ts, url, games)

def main():
	'''Checks to see if results are ready for each game or if there's a request error
	   and sends a message.'''
	msg = ''
	for game in ['numbers', 'win4']:
		while True:
			try:
				draw_data = request_json(game)
			except Exception as e:
				msg += str(e) + '\n'
				break
			if result_check(draw_data):
				msg += json_to_str(draw_data, game) + '\n'
				break
			print(f"Results not ready for {game}")
	msg += f"\n{timestamp()}"
	print(msg)
	twilio_text(msg)

if __name__ == '__main__':
	main()

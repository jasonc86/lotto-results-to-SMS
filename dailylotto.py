#!/usr/bin/python3
import requests
import time
import traceback
import sys
from twtxt import twilio_text

class dailyLotto:

	def __init__(self, game_name):
		'''initializes attributes for the data I want to send'''
		self.game_name = game_name
		self.json_url = f'https://nylottery.ny.gov/nyl-api/games/{game_name}/draws'
		self.draw_dict = {1: "Midday", 2: "Evening"}
		self.json_data = {}
		self.draw_period = ''
		self.results = ''
		# Error message if the program fails to get desired data
		err_url = f"https://nylottery.ny.gov/draw-game?game={self.game_name}."
		self.err_msg = f'Data unavailable.\nCheck results at\n{err_url}'
	
	def send_err(self):
		'''Sets result to error message'''
		self.results = self.err_msg
		
	def get_data(self):
		'''requests JSON data from url and returns results'''
		for x in range(4):
			try:
				res = requests.get(self.json_url, timeout=60)
				self.json_data = res.json()
				draw_data = self.json_data['data']['draws'][1]
				self.draw_period = self.draw_dict.get(draw_data['drawPeriod'], '')
				self.results = ''.join(draw_data['results'][0]['primary'])
				break
			except Exception:
				time.sleep(164) 
		else:
			print(traceback.format_exc())
			self.send_err()
		return f"{self.game_name.title()}: {self.results}\n"

	def get_draw(self):
		return f"{self.draw_period} {time.strftime('%x')}"

def sms_from_data():
	msg = ''
	games = ('numbers', 'win4')
	for game in games:
		dl = dailyLotto(game)
		msg += dl.get_data()
	msg += dl.get_draw()
	return msg

def main():
	msg = sms_from_data()
	print(msg)

if __name__ == '__main__':
	main()

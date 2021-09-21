#!/usr/bin/python3
'''Retrieves results for lottery games and sends the information to my phone via SMS.'''
from dailylotto import *
from twtxt import twilio_text

def main():
	'''Uses twilio to send lotto information.
	This was separated from dailylotto.py so I could test changes to that file
	without sending text messages.'''
	games = {'numbers':False, 'win4':False}
	format_sms(games, 30, 3600)
	twilio_text('\n\n'.join([v for v in games.values()]))

if __name__ == '__main__':
	main()

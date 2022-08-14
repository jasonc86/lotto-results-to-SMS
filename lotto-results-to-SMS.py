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
	msg = [v[0] for v in games.values()] # Contains winning numbers for each game
	msg += [v[1] for v in games.values()][1:] # Shows draw period and date for results
	#msg += [v[2] for v in games.values()][1:] # Shows draw period and date for results
	twilio_text('\n'.join(msg))

if __name__ == '__main__':
	main()

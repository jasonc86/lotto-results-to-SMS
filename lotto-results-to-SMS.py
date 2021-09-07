#!/usr/bin/python3
'''Retrieves results for lottery games and sends the information to my phone via SMS.'''
from dailylotto import *
from twtxt import twilio_text

def main():
	'''Uses twilio to send lotto information.
	This was separated from dailylotto.py so I could test changes to that file
	without sending text messages.'''
	games = {'numbers':False, 'win4':False}
	msg = format_sms(games)
	print(msg)
	twilio_text(msg)

if __name__ == '__main__':
	main()

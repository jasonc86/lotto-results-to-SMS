#!/usr/bin/python3
'''Module for sending string data to my phone as a text message via Twilio.
   Imported to dailylotto.py module'''
import sys
from os import environ as env
from twilio.rest import Client

def twilio_text(msg):
	'''Uses Twilio account info to send a text message to myself'''
	account_sid = env['TWID'] # Twilio ID
	auth_token = env['TWTOKEN'] # Twilio Authorization token
	client = Client(account_sid, auth_token)
	twi_no = env['TWNO'] # Twilio phone number
	cell_no = env['CELLNO'] # Actual cell phone number
	client.messages.create(body=msg, from_=twi_no, to=cell_no)

def main():
	'''takes data from standard input and sends it as a text message.
	   Main method is used mostly for testing.'''
	twilio_text(''.join(list(sys.stdin)).strip('\n'))

if __name__ == '__main__':
	main()

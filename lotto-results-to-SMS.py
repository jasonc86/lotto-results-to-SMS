#!/usr/bin/python3
'''Retrieves results for lottery games and sends the information to my phone via SMS.'''
from dailylotto import *
from twtxt import twilio_text

def main():
	msg = result_string()
	print(msg)
	twilio_text(msg)

if __name__ == '__main__':
	main()

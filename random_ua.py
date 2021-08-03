#!/usr/bin/python3
'''Module for randomly selecting user agent data
   for request headers from a json file'''
import json
from os import environ
from random import choice

def rand_user_agent():
	with open(f"{environ['HOME']}/dailylotto/user_agents.json") as f:
		list_ua = json.load(f)
	return choice(list_ua)

def main():
	print(rand_user_agent())

if __name__ == '__main__':
	main()

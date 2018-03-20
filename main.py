#!/usr/bin/env python

import sys
from subprocess import call
from threading import Thread
import socket

# Selenium
#import selenium.webdriver.chrome.service as service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# GPIO
from gpiozero import LED, Button
from time import sleep

public_ip = '10.3.141.1'
port = "16242"
groove_url = "http://" + public_ip + ":" + port + "/"
play_btn = 'nowplaying-toggle'
button_pin = 3
serverThread = None

def toggle_play(driver):
	driver.find_element_by_id(play_btn).click()

def getButtonFn(driver):
	def pressed(button):
		toggle_play(driver)
	return pressed

def startServer():
	call(["npm", "start", "--prefix", "/home/pi/Downloads/groovebasin/"])

def checkPort():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((public_ip, int(port)))
	except socket.error as e:
		return False
	s.close()
	return True

def main(arglist):
	global public_ip, port, groove_url, play_btn, button_pin, serverThread

	if 'runserver' in arglist:
		serverThread = Thread(target = startServer)
		if(checkPort() or ('force' in arglist)):
			serverThread.start()
			sleep(5)
			if(not checkPort() and ('force' not in arglist)):
				print("Couldn't start server!")
				exit(1)
		else:
			print("Port Occupied!")
			exit(1)
	
	if 'pin' in arglist:
		idx = arglist.index('pin')
		try:
			button_pin = int(arglist [idx + 1])
		except:
			print("Invalid pin no.")

	#service.start()
	opts = Options()
	opts.binary_location = '/usr/bin/chromium-browser'
	driver = webdriver.Chrome(chrome_options=opts)
	driver.get(groove_url)
	
	button = Button(button_pin)
	button.when_pressed = getButtonFn(driver)

if __name__ == '__main__':
	main(sys.argv)


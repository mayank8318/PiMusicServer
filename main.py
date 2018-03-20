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
# AUDIO DETECTION
import RPi.GPIO as GPIO
import time

public_ip = '10.3.141.1'
port = "16242"
groove_url = "http://" + public_ip + ":" + port + "/"
play_btn = 'nowplaying-toggle'
button_pin = 3
sound_module_pin = 15
serverThread = None

def setup_audio_detection(pin, driver):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN)
	GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=3000)  # let us know when the pin goes HIGH or LOW
	GPIO.add_event_callback(pin, getClapFn(driver))  # assign function to GPIO PIN, Run function on change

def toggle_play(driver):
	driver.find_element_by_id(play_btn).click()

def getClapFn(driver):
	def on_clap_detected(pin):
		toggle_play(driver)
		print("Clap!")
	return on_clap_detected

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
	global public_ip, port, groove_url, play_btn, button_pin, serverThread, sound_module_pin

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
	
	if 'pins' in arglist:
		idx = arglist.index('pins')
		try:
			button_pin = int(arglist [idx + 1])
			sound_module_pin = int(arglist [idx + 2])
		except:
			print("Invalid pin no.")

	#service.start()
	opts = Options()
	opts.binary_location = '/usr/bin/chromium-browser'
	driver = webdriver.Chrome(chrome_options=opts)
	driver.get(groove_url)
	
	button = Button(button_pin)
	button.when_pressed = getButtonFn(driver)
	setup_audio_detection(sound_module_pin, driver)

if __name__ == '__main__':
	main(sys.argv)


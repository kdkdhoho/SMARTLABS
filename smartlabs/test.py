import RPi.GPIO as GPIO
import threading
import Adafruit_DHT as dht
import time
import pigpio

# Thread
ledTh = threading.Thread()
airconTh = threading.Thread()
aircleanerTh = threading.Thread()
humidifierTh = threading.Thread()
doorTh = threading.Thread()
blindTh = threading.Thread()
dhtTh = threading.Thread()

# Mutex
ledLock=threading.Lock()
airconLock=threading.Lock()
aircleanerLock=threading.Lock()
humidifierLock=threading.Lock()
doorLock = threading.Lock()
blindLock=threading.Lock()
dhtLock=threading.Lock()

# Set up pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# led
led_1 = 25
led_2 = 16
led_3 = 19
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)
GPIO.setup(led_3, GPIO.OUT)

#door
door_state = "close"
door = 12
GPIO.setup(door, GPIO.OUT)
#door_servo = GPIO.PWM(door, 50) #door Pin use PWM using 50Hz

#blind
blind_state = "down"
blind = 13
GPIO.setup(blind, GPIO.OUT)
#blind_servo = GPIO.PWM(blind, 50) #blind Pin use PWM using 50Hz

#aircon
aircon_state = "off"
aircon = 23
GPIO.setup(aircon, GPIO.OUT)

#aircleaner
aircleaner_state = "off"
aircleaner = 20
GPIO.setup(aircleaner, GPIO.OUT)

#humidifier
humidifier = 18
GPIO.setup(humidifier, GPIO.OUT)

GPIO_dht = 6

def humidifierControl():
	global humidifierd, humidifierLock
	
	if (not humidifierLock.acquire(False)):
		return
		
	try:
		if (input(humidifier)):
			print("humidifier off")
			GPIO.output(humidifier, 0)
		else:
			print("humidifier on")
			GPIO.output(humidifier, 1)
			
		humidifierLock.release()
		
	except Exception as msg:
		print("humidifierThread ending....",msg)

def blindControl():
		global blind_servo, blindLock, blind_state, blind
		
		if (not blindLock.acquire(False)):
			return
			
		try:
			blind_servo = pigpio.pi()
			blind_servo.set_servo_pulsewidth(blind, 0)
			
			if (blind_state == "down"):
				print("Up Blind")
				blind_servo.set_servo_pulsewidth(blind, 600)
				blind_state = "up"
			else:
				print("Down Blind")
				blind_servo.set_servo_pulsewidth(blind, 2400)
				blind_state = "down"
				
			blindLock.release()
			
		except Exception as msg:
			print("blindThread ending....", msg)
			
def doorControl():
		global door_state, doorLock, door, door_servo
		
		if (not doorLock.acquire(False)):
				return
				
		try:
			door_servo = pigpio.pi()
			door_servo.set_servo_pulsewidth(blind, 0)
			
			if(door_state == "close"):
				print("open door")
				door_servo.set_servo_pulsewidth(door, 1500)
				door_state = "open"
			else:
				print("close door")
				door_servo.set_servo_pulsewidth(door, 2400)
				door_state = "close"

			doorLock.release()
				
		except Exception as msg:
				print("doorThread ending....", msg)
				
def dhtControl() :
	if (not dhtLock.acquire(False)):
		return
		
	try:
		for i in range(10):
			h, t = dht.read_retry(dht.DHT11, 6)
			print("\nTemper = {0:0.1f}*C  Humidity={1:0.1f}%" .format(t,h))
			time.sleep(1)
			
		dhtLock.release()
		
	except Exception as msg:
		print("dhtTH ending....", msg)

def ledControl():
		global led_1, led_2, led_3, ledLock
		
		if (not ledLock.acquire(False)):
				return
				
		try:
			ledNum = input("1 or 2 or 3 : ")
			
			if ledNum == "1":
				if GPIO.input(led_1) == 0:
					print("\nOn led 1")
					GPIO.output(led_1, 1)
				else:
					print("Off led 1")
					GPIO.output(led_1, 0)					
			elif ledNum == "2":
				if GPIO.input(led_2) == 0:
					print("\nOn led 2")
					GPIO.output(led_2, 1)
				else:
					print("Off led 2")
					GPIO.output(led_2, 0)	
			elif ledNum == "3":
					if GPIO.input(led_3) == 0:
						print("\nOn led 3")
						GPIO.output(led_3, 1)
					else:
						print("Off led 3")
						GPIO.output(led_3, 0)
						
			ledLock.release()
				
		except Exception as msg:
				print("ledThread ending....", msg)
				
def airconControl():
		global aircon, airconLock, aircon_state
		
		if (not airconLock.acquire(False)):
			return
				
		try:
			print("Control Aircon")
			
			if aircon_state == "off":
				print("Aircon On")
				GPIO.output(aircon, 0)
				aircon_state = "on"
			else:
				print("Aircon Off")
				GPIO.output(aircon, 1)
				aircon_state = "off"
				
			airconLock.release()
			
		except Exception as msg:
				print("airconThread ending....", msg)		
				
def 	aircleanerControl():
		global aircleaner, aircleanerLock, aircleaner_state
		
		if (not aircleanerLock.acquire(False)):
			return
				
		try:
			print("Control Aircleaner")
			
			if aircleaner_state == "off":
				print("Aircleaner On")
				GPIO.output(aircleaner, 0)
				aircleaner_state = "on"
			else:
				print("Aircleaner Off")
				GPIO.ouput(aircleaner, 1)
				aircon_state = "off"
				
			aircleanerLock.release()
			
		except Exception as msg:
			print("AircleanerThread ending....", msg)
				
			
def main():	
		try:
			while True:
					dhtTh = threading.Thread(target = dhtControl)
					dhtTh.start()
				
					choice = input("1: LED, 2: Aircon, 3: Humidifier, 4: Aircleaner, 5: Blind, 6: Door, 0: Quit  -> ")
					
					if choice == '1':
							ledTh = threading.Thread(target = ledControl)
							ledTh.start()
					elif choice == '2':
							airconTh = threading.Thread(target = airconControl)
							airconTh.start()
					elif choice == '3':
							humidifierTh = threading.Thread(target = humidifierControl)
							humidifierTh.start()
					elif choice == '4':
							aircleanerTh = threading.Thread(target = aircleanerControl)
							aircleanerTh.start()
					elif choice == '5':
							blindTh = threading.Thread(target = blindControl)
							blindTh.start()
					elif choice == '6':
							doorTh = threading.Thread(target = doorControl)
							doorTh.start()
					elif choice == '0':
							print("System Exit")
							break;
					else:
							print("Invalid Input")
								
		except KeyboardInterrupt:
				print("\nInterrupted! System Exit")
				return

main()
GPIO.cleanup()

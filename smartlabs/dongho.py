import RPi.GPIO as GPIO
import threading
#import Adafruit_DHT as dht
import time
import pigpio

# Thread
ledTh = threading.Thread()
airconTh = threading.Thread()
"""humidifierTh = threading.Thread()
aircleanerTh = threading.Thread()"""
doorTh = threading.Thread()
blindTh = threading.Thread()
dhtTh = threading.Thread()
# Mutex
ledLock=threading.Lock()
airconLock=threading.Lock()
"""humidifierLock=threading.Lock()
aircleanerLock=threading.Lock()"""
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
#door_servo = GPIO.PWM(door, 50) #door Pin use PWM using 50Hzaircon_A = 23

#blind
blind_state = "down"
blind = 13
GPIO.setup(blind, GPIO.OUT)
#blind_servo = GPIO.PWM(blind, 50) #blind Pin use PWM using 50Hz

#aircon
aircon_state = "off"
aircon = 23
GPIO.setup(aircon, GPIO.OUT)

"""humidifier = 18
GPIO.setup(humidifier, GPIO.OUT)

aircleaner_A = 20
aircleaner_B = 21
GPIO.setup(aircleaner, GPIO.OUT)"""

GPIO_dht = 6
global choice
choice=''

class dongho:
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
				door_servo.set_servo_pulsewidth(door, 1400)
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
	
	def main_dongho(self,x):	
		try:
			dhtTh = threading.Thread(target = dongho.dhtControl)
			dhtTh.start()
				
			print("1: LED, 2: Aircon, 3: Humidifier, 4: Aircleaner, 5: Blind, 6: Door, 0: Quit  -> ")
			global choice
			choice=int(x)
			
			if choice== 11:
				print("led1 on")
				ledTh = threading.Thread(target = dongho.ledControl)
				ledTh.start()
			elif choice== 12:
				print("led1 off")
			elif choice == 13:
				print("led2 on")
			elif choice== 14:
				print("led2 off")
			elif choice == 15:
				print("led3 on")
			elif choice == 16:
				print("led3 off")
			elif choice == 21:
				print("Aircon on")
				airconTh = threading.Thread(target = dongho.airconControl)
				airconTh.start()
			elif choice == 22:
				print("Aircon off")
			elif choice == 31:
				print("Humidfier on")
			elif choice== 32:
				print("Humidfier off")
			elif choice== 41:
				print("Aircleaner on")
			elif choice == 42:
				print("Aircleaner off")
			elif choice == 51:
				print("left curtain down")
				blindTh = threading.Thread(target = dongho.blindControl)
				blindTh.start()
			elif choice == 52:
				print("left curtain up")
			elif choice == 53:
				print("right curtain down")
			elif choice== 54:
				print("right curtain up")
			elif choice == 61:
				print("Door on")
				doorTh = threading.Thread(target = dongho.doorControl)
				doorTh.start()
			elif choice == 62:
				print("Door off")
			else:
				print("Invalid Input")
			"""
			if choice == '1':
				ledTh = threading.Thread(target = dongho.ledControl)
				ledTh.start()
			elif choice == '2':
				airconTh = threading.Thread(target = dongho.airconControl)
				airconTh.start()
			elif choice == '3':
				humidifierTh = threading.Thread(target = dongho.humidifierControl)
				humidifierTh.start()
			elif choice == '4':
				aircleanerTh = threading.Thread(target = dongho.aircleanerControl)
				aircleanerTh.start()
			elif choice == '5':
				blindTh = threading.Thread(target = dongho.blindControl)
				blindTh.start()
			elif choice == '6':
				doorTh = threading.Thread(target = dongho.doorControl)
				doorTh.start()
			elif choice == '0':
				print("System Exit")
			else:
				print("Invalid Input")
			"""	
							
		except KeyboardInterrupt:
			print("\nInterrupted! System Exit")
			return


dongho()
GPIO.cleanup()

import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensor = DHT.DHT11
pin = 6

mylcd = RPi_I2C_LCD_driver.lcd()2

try:
	while True:
		h, t = dht.read_retry(sensor, pin)
		
		if h is not None and t is not None:
			print("Temperature = {0:0.1f}*C, Humidity = {1:0.1f}%".format(t, h))
			#mylcd.lcd_display_string("Temp={0:0.1f}C".format(t, 1)
			#mylcd.lcd_display_string("Humidity={0:0.1f}%".format(h, 2)
		else: 
			print("Read error")
			
		time.sleep(1)
		
except KeyboardInterrupt:
	print("quit")
	GPIO.cleanup()

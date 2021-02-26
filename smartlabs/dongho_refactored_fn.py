import RPi.GPIO as GPIO
import threading
import Adafruit_DHT as dht
import time
import pigpio
# Set up pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Dongho():
    def __init__(self):
        self.info = Initializer()
        self.choice = -1
        self.selected_led = -1
        self.on_off = False

        # threads
        self.thread_list = [threading.Thread() for _ in range(7)]
        self.choice_waiter = threading.Thread(target=self.choice_wait, args=())
        self.choice_waiter.start()

        # targets
        self.target_list = [
            self.led_control, # 0
            self.aircon_control, # 1
            self.humidifier_control, # 2, not defined
            self.aircleaner_control, # 3, not difined
            self.blind_control, # 4
            self.door_control, # 5
            self.pir_control # 6
        ]

    def set_choice(self, num, on_off):
        tmp_choice = int(num)
        if tmp_choice > 7 or tmp_choice < -1 :
            print(tmp_choice, "Unknown order number")
        else :
            self.choice = tmp_choice
            self.on_off = bool(on_off)

    def choice_wait(self): 
        while True :
            if self.choice != -1:
                if self.choice == 7:
                    print("7, system exit")
                    break
                self.thread_list[self.choice] = threading.Thread(target=self.target_list[self.choice], args = (self.on_off,))
                self.thread_list[self.choice].start()
                self.choice = -1
                self.on_off = False
                
    def led_control(self, on_off): #0
        if self.select_led == -1:
            print("please select led num")
            return
        print("LED ", self.selected_led, " : activated")
        GPIO.output(self.info.led_pin_list[self.selected_led], on_off)

        self.selected_led=-1
   
    def aircon_control(self, on_off): #1
        GPIO.output(self.info.aircon_pin, on_off)

    def humidifier_control(self, on_off): #2, not defined
        pass

    def aircleaner_control(self, on_off): #3, not difined
        pass

    def blind_control(self, on_off): # 4
        self.blind_servo = pigpio.pi()
        self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 0)

        if on_off:
            self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 600)
        else :
            self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 2400)

    def door_control(self, on_off): # 5
        self.door_servo = pigpio.pi()
        self.door_servo.set_servo_pulsewidth(self.info.door_pin,0)
        
        if on_off:
            self.door_servo.set_servo_pulsewidth(self.info.door_pin, 1400)
        else :
            self.door_servo.set_servo_pulsewidth(self.info.door_pin, 2400)
           
    def pir_control(self, on_off): # 6
         while True:
           self.input_state = GPIO.input(self.info.pir_pin)
	       
           if on_off:
              if self.input_state == 0:
                  self.all_off()
           else:
              return
              
    def shutdown(self):
        self.all_off()
         
    def select_led(self, num):
        tmp_sl = int(num)
		
        if tmp_sl > 2 or tmp_sl < -1:
           print(tmp_sl, "Unknown led number")
        else:
           self.selected_led = tmp_sl
           
    def all_off(self):
        for i in range(3):
             GPIO.output(self.info.led_pin_list[i], False)
        GPIO.output(self.info.aircon_pin, True)
        self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 2400)
        self.door_servo.set_servo_pulsewidth(self.info.door_pin, 2400)
         
    # end of func
# end of Dongho class

class Initializer():
    def __init__(self):
        self.led_init()
        self.door_init()
        self.blind_init()
        self.aircon_init()
        self.pir_init()

    def led_init(self):
        self.led_pin_list = [25,16,19]
        
        for d in self.led_pin_list:
            GPIO.setup(d, GPIO.OUT)

    def door_init(self):
        self.door_pin = 12
        GPIO.setup(self.door_pin, GPIO.OUT)

    def blind_init(self):
        self.blind_pin = 13
        GPIO.setup(self.blind_pin, GPIO.OUT)

    def aircon_init(self):
        self.aircon_pin = 23
        GPIO.setup(self.aircon_pin, GPIO.OUT)
        
    def pir_init(self):
        self.pir_pin = 7
        GPIO.setup(self.pir_pin, GPIO.IN)
    
    #end of func
# end of Initializer class

if __name__ == "__main__":
    dh = Dongho()

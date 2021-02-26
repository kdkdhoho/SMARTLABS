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
        self.door_state = self.info.door_state
        self.blind_state = self.info.blind_state
        self.aircon_state = self.info.aircon_state
        self.choice = -1
        self.selected_led = -1

        # threads
        self.thread_list = [threading.Thread() for _ in range(6)]
        self.choice_waiter = threading.Thread(target=self.choice_wait, args=())
        self.choice_waiter.start()

        # targets
        self.target_list = [
            self.led_control, # 0
            self.aircon_control, # 1
            self.humidifier_control, # 2, not defined
            self.aircleaner_control, # 3, not defined
            self.blind_control, # 4 
            self.door_control, # 5
        ]

    def set_choice(self, num):
        tmp_choice = int(num)
        if tmp_choice > 7 or tmp_choice < -1 :
            print(tmp_choice, "Unknown order number")
        else :
            self.choice = tmp_choice

    def choice_wait(self):
        try:
            while True :
                if self.choice != -1:
                    if self.choice == 7:
                        print("7, system exit")
                        break
                    print(self.choice)
                    self.thread_list[self.choice] = threading.Thread(target=self.target_list[self.choice])
                    print(self.thread_list[self.choice] )
                    print(self.target_list[self.choice] )
                    self.thread_list[self.choice].start()
                    self.choice = -1

        except KeyboardInterrupt:
            print("System exited due to Ctrl+C operation")

    def led_control(self): #0
        if self.select_led == -1:
            print("please select led num")
            return
        print("LED ", self.selected_led, " : activated")
        if GPIO.input(self.info.led_pin_list[self.selected_led]) == 0:
            GPIO.output(self.info.led_pin_list[self.selected_led], 1)
        else : 
            GPIO.output(self.info.led_pin_list[self.selected_led], 0)

        self.selected_led=-1
   
    def aircon_control(self): #1
        print("cp1")
        if self.info.aircon_state:
            GPIO.output(self.info.aircon_pin, 1)
            self.info.aircon_state = False
        else :
            GPIO.output(self.info.aircon_pin, 0)
            self.info.aircon_state = True

    def humidifier_control(self): #2, not defined
        pass

    def aircleaner_control(self): #3, not defined
        pass

    def blind_control(self): # 4
        self.blind_servo = pigpio.pi()
        self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 0)

        if self.info.blind_state:
            self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 2400)
            self.info.blind_state = False
        else :
            self.blind_servo.set_servo_pulsewidth(self.info.blind_pin, 600)
            self.info.blind_state = True

    def door_control(self): # 5
        self.door_servo = pigpio.pi()
        self.door_servo.set_servo_pulsewidth(self.info.door_pin,0)

        if self.info.door_state:
            self.door_servo.set_servo_pulsewidth(self.info.blind_pin, 2400)
            self.dh.self.info.door_state=True
        else :
            self.door_servo.set_servo_pulsewidth(self.info.blind_pin, 1400)
            self.dh.self.info.door_state=False

    def select_led(self, num):
        tmp_sl = int(num)
        if tmp_sl > 2 or tmp_sl < -1 :
            print(tmp_sl, "Unknown led number")
        else :
            self.selected_led = tmp_sl  
    # end of func
# end of Dongho class    

class Initializer():
    def __init__(self):
        self.led_init()
        self.door_init()
        self.blind_init()
        self.aircon_init()

    def led_init(self):
        self.led_pin_list = [25,16,19]

        for d in self.led_pin_list:
            GPIO.setup(d, GPIO.OUT)

    def door_init(self):
        self.door_state = False # close
        self.door_pin = 12
        GPIO.setup(self.door_pin, GPIO.OUT)

    def blind_init(self):
        self.blind_state = False # down
        self.blind_pin = 13
        GPIO.setup(self.blind_pin, GPIO.OUT)

    def aircon_init(self):
        self.aircon_state = False # off
        self.aircon_pin = 23
        GPIO.setup(self.aircon_pin, GPIO.OUT)

    # def humidifier_init ~~ 니가 만드셈
    #end of func
# end of Initializer class

if __name__ == "__main__":
    dh = Dongho()
    dh.set_choice(1)


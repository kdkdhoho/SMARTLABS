import server_module as sm
import multiprocessing as mp
import dongho_refactored_fn as dh

class module_communicator:
	def __init__(self):
		self.dh=dh.Dongho()
		self.server = sm.socket_server()
		self.command=""
		self.communicate()

	def communicate(self):
		while True:
			if self.server.ch != None :
				self.command = self.server.ch.get_client_msg()
			if self.command != "" :
				self.command = int(self.command)

			if self.command != "" :
				print(self.command)
				if self.command > 10 and self.command <20:	
					if self.command==11:
						self.dh.select_led(0)
						self.dh.set_choice(0, True)
					elif self.command==12:
						self.dh.select_led(0)
						self.dh.set_choice(0, False)
					elif self.command==13:
						self.dh.select_led(1)
						self.dh.set_choice(0, True)
					elif self.command==14:
						self.dh.select_led(1)
						self.dh.set_choice(0, False)
					elif self.command==15:
						self.dh.select_led(2)
						self.dh.set_choice(0, True)
					elif self.command==16:
						self.dh.select_led(2)
						self.dh.set_choice(0, False)				
					else:
						print("main module : command ->", self.command)
				
				# aircon
				elif self.command==21: 
					self.dh.set_choice(1,False)
				elif self.command==22:	
					self.dh.set_choice(1,True)
					
				# set_choice(2), (3) not defined
				
				# blind
				elif self.command==53: 
					self.dh.set_choice(4,True)
				elif self.command==54:	
					self.dh.set_choice(4,False)
					
				# door
				elif self.command==61:
					self.dh.set_choice(5,True)
				elif  self.command==62:
					self.dh.set_choice(5,False)
					
				# pir (Automode)
				elif self.command == 76:
					self.dh.set_choice(6, True)
				elif self.command == 77:
					self.dh.set_choice(6, False)
					
				# all off
				elif self.command == 88:
					self.dh.shutdown()
					
				self.command=""
	
if __name__ == '__main__':
	
	module_communicator()

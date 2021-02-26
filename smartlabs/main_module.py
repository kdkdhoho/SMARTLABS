import server_module as sm
import multiprocessing as mp
import dongho_refactored as dh

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
					if self.command==11 or self.command==12:
						self.dh.select_led(0)
					elif self.command==13 or self.command==14:
						self.dh.select_led(1)
					elif self.command==15 or self.command==16:
						self.dh.select_led(2)					
					else:
						print("main module : command ->", self.command)
					self.dh.set_choice(0)
				elif self.command==21 or self.command ==22:	
					self.dh.set_choice(1)
				elif self.command==53 or self.command==54: # set_choice(2),(3) not defined
					self.dh.set_choice(4)
				elif self.command==61 or self.command==62:
					self.dh.set_choice(5)
					
				self.command=""
	
if __name__ == '__main__':
	
	module_communicator()

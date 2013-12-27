import argparse
import random
import socket

__version__ = '0.2'

class ChatTcp:
	def __init__(self, port, ip = None):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if ip:
			self.peer_addr = (ip, port)
			self.sock.connect(self.peer_addr)
		else:
			self.server_sock = self.sock
			self.server_sock.bind(('0.0.0.0', port))
			self.server_sock.listen(1)
			self.sock, self.peer_addr = self.server_sock.accept()

	def send_message(self, message):
		self.sock.send(message)

	def get_message(self):
		message = self.sock.recv(1025)
		return message

class ChatUdp:
	def __init__(self, port, ip = None):
		self.peer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if ip:
			self.peer_sock.bind(('0.0.0.0', random.randint(20000, 50000)))
			self.peer_addr = (ip, port)
		else:
			self.peer_sock.bind(('0.0.0.0', port))
		self.sock = self.peer_sock

	def get_message(self):
		message, self.peer_addr = self.sock.recvfrom(1025)
		return message

	def send_message(self, message):
		self.sock.sendto(message, self.peer_addr)

def main():
	parser = argparse.ArgumentParser(description = '', conflict_handler = 'resolve')
	parser.add_argument('-v', '--version', action = 'version', version = parser.prog + ' Version: ' + __version__)
	parser.add_argument('-V', '--verbose', dest = 'verbose', action = 'store_true', default = False, help = 'enable verbose output')
	parser.add_argument('-u', '--udp', dest = 'chat_udp', action = 'store_true', default = False, help = 'choses udp or tcp')
	parser.add_argument('-p', '--port', dest = 'port', type = int,  required = True, help = 'Choose port to listen on')
	parser.add_argument('-i', '--ip', dest = 'ip', help = 'Chooses ip')
	args = parser.parse_args()
	if args.chat_udp:
		chat = ChatUdp(args.port, args.ip)
	else:
		chat = ChatTcp(args.port, args.ip)
	if args.ip:
		message = raw_input('you > ')
		chat.send_message(message)
	while True:
		message = chat.get_message()
		print(chat.peer_addr[0] + ":" + str(chat.peer_addr[1]) + " > " + message)
		message = raw_input('you > ')
		chat.send_message(message)
	return 0

if __name__ == '__main__':
	main()


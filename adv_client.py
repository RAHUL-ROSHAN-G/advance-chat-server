from multiprocessing import Condition
import socket
import threading

nickname = input("Choose a nickname: ")
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if nickname == 'admin':
	password = input('Enter password for admin: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 55555))
stop_thread = False

def receive():
	Condition = True
	while Condition:
		global stop_thread
		if stop_thread:
			break
		try:
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
				next_message =client.recv(1024).decode('ascii')
				if next_message == "PASS":
					client.send(password.encode('ascii'))
					if client.recv(1024).decode('ascii') == 'REFUSE':
						print("Connection was refused! wrong password")
						stop_thread = True
				elif next_message == 'BAN':
					print('Connection refuse becasue of ban!')
					client.close()
					stop_thread = True	
			else:
				print(message)
		except:
			print("An error ocuured")
			client.close()
			break

def write():
	Condition = True
	while Condition:
		if stop_thread:
			break
		message = f'{nickname}: {input(" ")}'
		if message[len(nickname)+2:].startswith('/'):
			if nickname == "admin":
					if message[len(nickname)+2:].startswith('/kick'):
						client.send(f'KICK {message[len(nickname)+2+6: ]}'.encode('ascii'))
					elif message[len(nickname)+2:].startswith('/ban'):
						client.send(f'BAN {message[len(nickname)+2+5: ]}'.encode('ascii'))	
			else:
				print("Commands can only be the executed by the admin. ")
		#elif message == 'quit':
		#	Condition = False
		else:
			client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

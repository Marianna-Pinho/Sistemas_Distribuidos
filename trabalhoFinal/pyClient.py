#!/usr/bin/env python
import pika
import json
import uuid
import os

SUCCESS = "success"
FAIL = "fail"

################################## TELAS ###################################
#First options shown to the user.
def loginSCREEN():
	print("========== AGENDA ==========")
	print("\t 1-Entrar \t")
	print("\t 2-Cadastrar\t")
	print("============================\n")

#Screen shown when the user is logged.
def optionSCREEN():
	print("========================== AGENDA =====================")
	print("\t 1 - Cadastrar eventos por hora e data")
	print("\t 2 - Adicionar participantes por evento")
	print("\t 3 - Listar participantes por evento")
	print("\t 4 - Remover participantes por evento")
	print("\t 5 - Listar presentes no evento")
	print("\t 6 - Listar eventos por dia")
	print("\t 7 - Fazer checkin no evento")
	print("\t 8 - Logout")
	print("=======================================================\n")

################################### SERIALIZER #############################
#Function used to translate data to JSON format, with the kind of service asked and the correspondent necessary parameters.
def serializeData(operation, *args):
	if((operation == "entrar") or (operation == "cadastrar")):
		data = {"operation": operation,
				"username": args[0],
				"password": args[1]}

	elif(operation == "addEvent"):
		data = {"operation": operation,
				"eventName": args[0],
				"eventDate": args[1],
				"eventHour": args[2]}

	elif(operation == "client2Event"):
		data = {"operation": operation,
				"username": args[0],
				"eventName": args[1]}

	elif(operation == "listParticipants"):
		data = {"operation": operation,
				"eventName": args[0]}

	elif(operation == "removeParticipants"):
		data = {"operation": operation,
				"username":	args[0],
				"eventName": args[1]}

	elif(operation == "listPresents"):
		data = {"operation": operation,
				"eventName": args[0]}

	elif(operation == "listEvents"):
		data = {"operation": operation,
				"eventDate": args[0]}

	elif(operation == "checkin"):
		data = {"operation": operation,
				"username": args[0],
				"eventName": args[1]}

	elif(operation == "logout"):			
		data = {"operation": operation,
				"username": args[0]}

	#This translates the dictionary created to JSON structure.
	return json.dumps(data)

#Function used to translate json data received from server to a dictionary. The answer has a status (talks about success of operation) and a response.
def deserializeData(jsonMessage):
	message = json.loads(jsonMessage)
	return message['status'], message['response']

class pyClient:

	Username = ""
	Password = ""

#################################### INTERACAO #########################################
	#Function used to set RABBITMQ parameters, like the kind of connection, the queue and the form of use of the queue.
	def __init__(self):
		self.credentials = pika.PlainCredentials('client01', 'sdec')
		#This is used to allow use remote machines. However, the broker(RABBITMQ) is local.
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.120.117', 5672, '/', self.credentials)) #You need change this parameters when running in your machine. You can use 'localhost'.
		self.channel = self.connection.channel()
		result = self.channel.queue_declare(exclusive=True)
		self.callback_queue = result.method.queue
		#We are creating a callback queue to receive the answers from server.
		self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

	#Function used to store the answer from server.
	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	#Function used to send requests to the server.
	def sendMessage(self, serialMessage):
		self.response = None
		self.corr_id = str(uuid.uuid4())

		self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                   		content_type = "application/json",
                                        reply_to = self.callback_queue,
                                        correlation_id = self.corr_id,
                                        ),
                                   body= serialMessage)

		#This blocks the function, making her wait the answer from server.
		while self.response is None:
			self.connection.process_data_events()
		return self.response

################################### SERVICE INTERFACES ####################################
	#Function used to ask user login.
	def loginClient(self,operation):
		print("========= LOGIN ========")
		self.Username = raw_input('Username:')
		self.Password = raw_input('Password:')
		os.system('clear')

		jsonOBJ = serializeData(operation, self.Username, self.Password)
		#This sends the message to the server, after translate the data to JSON format.
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)
		
	#Function used to get the necessary information to register an event.
	def registerEvent(self, operation):
		print("================== REGISTER EVENT =================")
		eventName = raw_input('Event Name:')
		eventDate = raw_input('Date of the event: [format DD-MM-YY]\n')
		eventHour = raw_input('Hour of the event: [format hh:mm]\n')
		os.system('clear')

		jsonOBJ = serializeData(operation, eventName, eventDate, eventHour)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to get the necessary information to associate a user with an event.
	def client2Event(self, operation):
		print("============== ADD PARTICIPANT TO EVENT =============")
		eventName = raw_input('Event Name:')
		os.system('clear')

		jsonOBJ = serializeData(operation, self.Username, eventName)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to get the necessary information to list all the participants of an event. 
	def listPartEvent(self, operation):
		print("============== LIST PARTICIPANTS OF AN EVENT =============")
		eventName = raw_input('Event Name:')
		os.system('clear')

		jsonOBJ = serializeData(operation, eventName)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to get the necessary information to remove a participant from an event.
	def removePart(self, operation):
		print("============== REMOVE PARTICIPANT OF AN EVENT =============")
		eventName = raw_input('Event Name:')
		os.system('clear')

		jsonOBJ = serializeData(operation, self.Username, eventName)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to get the necessary information to list all  present participants in an event.
	def listPresEvent(self, operation):
		print("============== LIST PRESENTS IN AN EVENT =============")
		eventName = raw_input('Event Name:')
		os.system('clear')

		jsonOBJ = serializeData(operation, eventName)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to get the necessary information to list all events of an specific date.
	def listEventDay(self, operation):
		print("============== LIST EVENTS IN A DAY =============")
		eventDate = raw_input('Date of the event: [format DD-MM-YY]\n')
		os.system('clear')

		jsonOBJ = serializeData(operation, eventDate)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to get the necessary information allow user do its check in.
	def doCheckin(self, operation):
		print("============== CHECKIN =============")
		eventName = raw_input('Event Name:')
		os.system('clear')

		jsonOBJ = serializeData(operation, self.Username, eventName)
		response = self.sendMessage(jsonOBJ)
		return deserializeData(response)

	#Function used to do the logout.
	def doLogout(self, operation):
		print("------------ LOGOUT ------------")
		jsonOBJ = serializeData(operation, self.Username)


#"Main" function, responsible to show the services to the user, identify the kind of service requested and treat success or fail of operations.
def main():
	option = 0
	client = pyClient()

##################### LOGIN and SIGN UP ########################	
	while(1):
		while(option == 0):
			loginSCREEN()
			option = raw_input()		#Read option (Login or Cadastro)
			os.system('clear')

			if(option == '1'):
				status, resp = client.loginClient("entrar")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
					option = 0	
			elif(option == '2'):
				status, resp = client.loginClient("cadastrar")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
					option = 0
			else:
				option = 0
				print("You choose a nonexistent option. Try it again!")
				

		print("\n" + resp + "\n")
		option = 0


	###################### SERVICES ##########################
		while(option != '8'):
			optionSCREEN()
			option = raw_input()
			os.system('clear')
			
			if(option == '1'):
				status, resp = client.registerEvent("addEvent")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '2'):
				status, resp = client.client2Event("client2Event")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '3'):
				status, resp = client.listPartEvent("listParticipants")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '4'):
				status, resp = client.removePart("removeParticipants")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '5'):
				status, resp = client.listPresEvent("listPresents")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '6'):
				status, resp = client.listEventDay("listEvents")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '7'):
				status, resp =  client.doCheckin("checkin")
				if(status == "FAIL"):
					print("\n" + resp + "Try it again!\n")
			elif(option == '8'):
				client.doLogout("logout")
			else:
				print("\tOption nonexistent. Try it again!")

			if(status == "SUCCESS"):
				print("=================== ANSWER =================")
				print("\n" + resp + "\n")	
		option = 0

main()

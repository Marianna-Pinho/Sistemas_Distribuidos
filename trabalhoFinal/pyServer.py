#!/usr/bin/env python
import pika
import json
import os

#Function used to serialize data to be sent. The format adopted is JSON.
def serializeData(status, message):
    data = {"status": status,
            "response": message}
    return json.dumps(data)

class pyServer:
##################################### INTERACAO #################################
    #Function used to set RABBITMQ parameters, like the kind of connection, the queue and the form of use of the queue.
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue='rpc_queue')
    
    #Function used to describe what to do when a request is received.
    def on_request(self, ch, method, props, body):
        jsonMessage = body
        print("------------ PROCESSING -------------")
            
        self.response = self.processRequest(jsonMessage) #processRequest deals with the data received.

        #This says what to answer and where do it.
        ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                    props.correlation_id,
                                    content_type = "application/json"),
                    body=self.response)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        print("Waiting messages...")

    #Function responsible of starts server.
    def runServer(self):
        print("Waiting messages...")
        self.channel.start_consuming()
 

    #Function used to identify the kind of service.
    def processRequest(self, jsonMessage):
    	#this translate a json message to a dictionary.
        message = json.loads(jsonMessage)
       
        if(message['operation'] == "entrar"):            
            return self.authenticate(message)
        elif(message['operation'] == "cadastrar"):
            return self.registerUser(message)
        elif(message['operation'] == "addEvent"):
            return self.registerEvent(message)
        elif(message['operation'] == "client2Event"):
            return self.client2Event(message)
        elif(message['operation'] == "listParticipants"):
            return self.listPartEvent(message)
        elif(message['operation'] == "listEvents"):
            return self.listEventDay(message)
        elif(message['operation'] == "checkin"):
            return self.doCheckin(message)
        elif(message['operation'] == "listPresents"):
            return self.listPresEvent(message)
        elif(message['operation'] == "removeParticipants"):
            return self.removeParts(message)
            


######################################## AUXILIAR SERVICES ###################################
	#Function used to verify the existence of a user, when someone tries to do the login.
    def authenticate(self, message):
        with open('data.txt') as json_file:
            if(os.stat("data.txt").st_size == 0):
            	#All data is serialized (translated to JSON) to be sent.
                return serializeData("FAIL", "YOU AREN'T REGISTERED!")
            data = json.load(json_file)

            for user in data['user']:
                if(user['username'] == message['username']):
                    if(user['password'] == message['password']):
                        return serializeData("SUCCESS", "CLIENT LOGGED!")
                    else:
                        return serializeData("FAIL", "WRONG PASSWORD!")
            json_file.close()
            return serializeData("FAIL", "YOU AREN'T REGISTERED!")
#==================================================================================================
	#Auxiliar function used to add a user, in a pre-determined format.
    def createUser(self, message, data):
        data['user'].append({'username': message['username'], 'password': message['password']})
        return data 

    #Function used to register a new user. If the username already exists, the user won't be registered.
    def registerUser(self, message):
        data = {}
        data['user'] = []

        with open('data.txt') as json_file:
            if(os.stat("data.txt").st_size == 0):
                data = self.createUser(message, data)
            else:
                data = json.load(json_file)
                for user in data['user']:
                    if(user['username'] == message['username']):
                        return serializeData("FAIL", "CLIENT ALREADY EXIST!")

                data = self.createUser(message, data)
            json_file.close()

        with open('data.txt','w') as json_file:
            json.dump(data, json_file, indent = 4)
            json_file.close()
        return serializeData("SUCCESS", "CLIENT REGISTERED!")

#==================================================================================================
	#Auxiliar function used to add an event, in a pre-determined format.
    def createEvent(self, message, data):

        data['event'].append({'eventName': message['eventName'], 'eventDate': message['eventDate'],
                             'eventHour': message['eventHour'], 'participants': [], 'presents': []})
        return data 

    #Function used to register a new event. If the eventName already exists, the event won't be registered.
    def registerEvent(self, message):
        data = {}
        data['event'] = []

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                data = self.createEvent(message, data)
            else:
                data = json.load(json_file)
                for event in data['event']:
                    if(event['eventName'] == message['eventName']):
                        return serializeData("FAIL", "EVENT ALREADY EXIST!")

                data = self.createEvent(message, data)
            json_file.close()

        with open('eventos.txt','w') as json_file:
            json.dump(data, json_file, indent = 4)
            json_file.close()
        return serializeData("SUCCESS", "EVENT REGISTERED!")       
#==================================================================================================
	#Auxiliar function used to add a participant to an event, in a pre-determined format.
    def includeClient(self, message, data):
        data['participants'].append(message['username'])
        return data

    #Function used to associate an user to an event. Only the own user can add itself to an event.
    def client2Event(self, message):
        data = {}
        dataAux = {}
        data['event'] = []
        dataAux['event'] = []
        flag = False

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")

            data = json.load(json_file)
            for event in data['event']:
                if(event['eventName'] == message['eventName']):
                    if((message['username'] in event['participants']) == False):
                        dataAux['event'].append(self.includeClient(message, event))
                        flag = True
                    else:
                        return serializeData("FAIL", "PARTICIPANT ALREADY REGISTERED ON EVENT!")
                    continue
                dataAux['event'].append(event)
            
            if(flag == False):
                return serializeData("FAIL", "EVENT DIDN'T FOUND!") 
            json_file.close()
        with open('eventos.txt','w') as json_file:
            json.dump(dataAux, json_file, indent = 4)
            json_file.close() 
        return serializeData("SUCCESS", "PARTICIPANT REGISTERED ON EVENT!")           
#==================================================================================================
	#Auxiliar function used to translate a set of information to a string.
    def toString(self, msgList):
        message = ""
        for p in msgList:
            message = message + p + "\n"
        return message

    #Function used to give a list of participants of an event.
    def listPartEvent(self, message):
        data = {}
        data['event'] = []

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")

            data = json.load(json_file)
            json_file.close()

            for event in data['event']:
                if(event['eventName'] == message['eventName']):
                    if(len(event['participants']) == 0):
                        return serializeData("FAIL", "NO PARTICIPANTS REGISTERED!")

                    return serializeData("SUCCESS", self.toString(event['participants']))
            return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")
#==================================================================================================
	#Function used to list a set of events scheduled for a date.
    def listEventDay(self, message):
        data = {}
        data['event'] = []
        eventNames = []

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                return serializeData("FAIL", "NO EVENTS REGISTERED!")

            data = json.load(json_file)
            json_file.close()

            for event in data['event']:
                if(event['eventDate'] == message['eventDate']):
                    eventNames.append(event['eventName'])

            if(len(eventNames) == 0):
                 return serializeData("FAIL", "NO EVENTS REGISTERED ON THIS DATE!")
            return serializeData("SUCCESS", self.toString(eventNames))

#==================================================================================================
	#Auxiliar funcion used to add a present participant, in a pre-determined format.
    def includePresent(self, message, data):
        data['presents'].append(message['username'])
        return data

    #Function used to say that a participant of an event was present in the event. The own user must do the check in.
    def doCheckin(self, message):
        data = {}
        dataAux = {}
        data['event'] = []
        dataAux['event'] = []
        flag = False

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")

            data = json.load(json_file)
            for event in data['event']:
                if(event['eventName'] == message['eventName']):
                    if(((message['username'] in event['presents']) == False)):
                        if((message['username'] in event['participants']) == True):
                            dataAux['event'].append(self.includePresent(message, event))
                            flag = True
                        else:
                            return serializeData("FAIL", "YOU AREN'T A PARTICIPANT OF THIS EVENT!")
                    else:
                        return serializeData("FAIL", "PARTICIPANT ALREADY PRESENT ON EVENT!")
                    continue
                dataAux['event'].append(event)
            
            if(flag == False):
                return serializeData("FAIL", "EVENT DIDN'T FOUND!") 
            json_file.close()
        with open('eventos.txt','w') as json_file:
            json.dump(dataAux, json_file, indent = 4)
            json_file.close() 
        return serializeData("SUCCESS", "CHECKIN ON EVENT!")           
#==================================================================================================
	#Function used to list all the presents in an event.
    def listPresEvent(self, message):
        data = {}
        data['event'] = []

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")

            data = json.load(json_file)
            json_file.close()

            for event in data['event']:
                if(event['eventName'] == message['eventName']):
                    if(len(event['presents']) == 0):
                        return serializeData("FAIL", "NO PRESENTS ON THIS EVENT!")

                    return serializeData("SUCCESS", self.toString(event['presents']))
            return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")

#==================================================================================================
	#Function used to remove a participant from an event.
    def removeParts(self, message):
        data = {}
        dataAux = {}
        data['event'] = []
        dataAux['event'] = []
        flag = False

        with open('eventos.txt') as json_file:
            if(os.stat("eventos.txt").st_size == 0):
                return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")

            data = json.load(json_file)
            json_file.close()

            for event in data['event']:
                if(event['eventName'] == message['eventName']):
                    if((message['username'] in event['participants']) == True):
                        event['participants'].remove(message['username'])
                        flag = True
                    else:
                        return serializeData("FAIL", "YOU AREN'T REGISTERED IN THIS EVENT!")
                dataAux['event'].append(event)

            if(flag):
                with open('eventos.txt','w') as json_file:
                    json.dump(dataAux, json_file, indent = 4)
                    json_file.close() 
                return serializeData("SUCCESS", "PARTICIPANT REMOVED!")
            return serializeData("FAIL", "EVENT DOESN'T REGISTERED!")



#"Main" function, used to create the server and initialize it.
def main():
    server = pyServer()
    server.runServer()
   
main()
#Connection Agent for Robots, by Stephen M. Wanser
import time
import os
import sqlite3
import serial
import datetime

class robotConnectionAgent(object):

    def __init__(self):

        print("Robotic Firmware Communicator Agent Initialized!")
        self.initializeDatabaseConnection()
        self.initializeSerialConnection()
        
    def initializeDatabaseConnection(self):
        
        print("Initializing connection to database...")
        try:
            if os.path.isfile("messages.db"):
                print("Previous database found! Connecting to existing database.")
                self.con = sqlite3.connect("messages.db")
                self.cur = self.con.cursor()
                print("Database connection established successfully.")
                self.databaseConnected = True
                
            else:
                print("No database found...creating new one!")
                self.con = sqlite3.connect("messages.db")
                self.cur = self.con.cursor()
                self.cur.execute("CREATE TABLE outbound(id INTEGER PRIMARY KEY AUTOINCREMENT, commandMessage STRING, currentDate DATE, currentTime TIME, processed INTEGER)")
                self.con.commit()
                self.cur.execute("CREATE TABLE inbound(id INTEGER PRIMARY KEY AUTOINCREMENT, signalMessage STRING, currentDate DATE, currentTime TIME, referenceID INTEGER)")
                self.con.commit()
                print("Database initialized and connection established successfully.")
                self.databaseConnected = True
                
        except Exception as E:
            print("Error initialzing connection to database:", E)
            self.databaseConnected = False

    def initializeSerialConnection(self):
    
        print("Initializing Serial Connection...")
        initialized = False
        comPort = ['COM3', 'COM4', 'COM5', 'COM2', 'COM1']
        counter = 0
        while not initialized and counter < len(comPort):
            
            try:
                arduinoConnection = True
                self.microCon = serial.Serial(comPort[counter])
                self.microCon.flushInput()
                print("Serial Connection Initialized on", comPort[counter] + "!")
                initialized = True
                self.serialConnected = True
                
            except Exception as E:
                counter = counter + 1
                print("Error initializing connection to Arduino:", E)
                self.serialConnected = False

    def monitor(self):

        print("Initializing Live Monitoring of Database and Serial...")
        while self.databaseConnected and self.serialConnected:

            self.processOutboundCommands()
            self.processIncomingMessages()

    def processOutboundCommands(self):

        try:
            queryStatement = "SELECT * FROM outbound WHERE processed = 0;"

            queryResults = self.cur.execute(queryStatement)
        except Exception as E:
            print("Error during outbound command processing while querying database:", E)
        
        try:
            for row in queryResults:
                command = row
                print("Processing outbound command:", command)
                self.transmitCommand(command[1])
                insertStatement = "UPDATE outbound SET processed = 1 where id = ?"
                dataValues = [command[0]]
                self.cur.execute(insertStatement, dataValues)
                self.con.commit()
                print("Command processed!")
                            
        except Exception as E:
            print("Error during outbound command processing while transmitting via Serial:", E)

    def processIncomingMessages(self):

        if self.microCon.in_waiting > 0:
                message = self.microCon.readline()
                message = message[:-2].decode("utf-8")
                print(message)
                dtg = datetime.datetime.now()
                dateString = dtg.strftime("%Y-%m-%d")
                timeString = dtg.strftime("%H:%M:%S")
                insertStatement = "INSERT INTO inbound(signalMessage,currentDate,currentTime,referenceID) VALUES(?,?,?,?)"
                dataValues = [message, dateString, timeString, 1]
                self.cur.execute(insertStatement, dataValues)
                self.con.commit()
                
    def transmitCommand(self, commandMessage):

        if self.serialConnected == True:

            self.microCon.write(commandMessage.encode())

if __name__ == "__main__":
    
    agent = robotConnectionAgent()
    agent.monitor()

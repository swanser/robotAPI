from flask import Flask
import os, subprocess
import serial
import sqlite3
import datetime
import uuid
import json

def controllerAPI():

    app = Flask(__name__)

    @app.route('/')
    def healthCheck():
        return "UP"
    
    @app.route('/<servo>/<directive>/<detail>')
    def command(servo, directive, detail):

        if servo.upper() == "JAW" or servo.upper() == "EYESV" or servo.upper() == "EYESH" or servo.upper() == "NECKPIVOT":
            if directive.upper() == "MOVE" or directive.upper() == "PIN" or directive.upper() == "SPEED":
                
                if servo.upper() == "JAW":
                    servo = "C"
                elif servo.upper() == "EYESV":
                    servo = "B"
                elif servo.upper() == "EYESH":
                    servo = "A"
                elif servo.upper == "NECKPIVOT":
                    servo = "D"

                if directive.upper() == "MOVE":
                    directive = "M"
                elif directive.upper() == "PIN":
                    directive = "P"
                elif directive.upper() == "SPEED":
                    directive = "S"
                    
                commandReferenceID = uuid.uuid4()
                commandString = directive + servo + detail + ';'
                issueCommand(commandString, str(commandReferenceID)[0:13])

                return str(commandReferenceID)[0:13]
            else:
                return "DIRECTIVE NOT FOUND!"
        else:
            return("SERVO NOT FOUND!")

    @app.route('/results/<referenceID>')
    def checkCommandResults(referenceID):

        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        try:
            queryStatement = "SELECT * FROM inbound WHERE referenceID = ?;"
            print("Query statement:", queryStatement)
            values = [referenceID,]

            queryResults = cur.execute(queryStatement, values)
            print("queryStatment",queryStatement,"\nvalues:", values)
            results = queryResults.fetchall()
            print('Results len:', len(results))
            if len(results) == 0:
                return("NO RESULTS FOUND FOR QUERY ID " + referenceID)
            for row in results:
                print(row)
            return(json.dumps(results[0]))
        except Exception as E:
            print("Error during inbound command processing while querying database:", E)
            return(str(E))
        

    def issueCommand(command, referenceID):

        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        dtg = datetime.datetime.now()

        dateString = dtg.strftime("%Y-%m-%d")
        timeString = dtg.strftime("%H:%M:%S")
        insertStatement = "INSERT INTO outbound(commandMessage,currentDate,currentTime, processed, referenceID) VALUES(?,?,?,?,?)"
        dataValues = [command,dateString,timeString, 0, referenceID]
        cur.execute(insertStatement, dataValues)
        con.commit()
        con.close()

    return app

API = controllerAPI()

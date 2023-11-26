from flask import Flask
import os, subprocess
import serial
import sqlite3
import datetime



def headControllerAPI():

    app = Flask(__name__)

    @app.route('/')
    def healthCheck():
        return "UP"
    
    @app.route('/MOVE/<moveCommand>')
    def moveCommand(moveCommand):

        if moveCommand == "JAWMAX":
            issueCommand("MOVEJAWMAX")
            return "MOVEJAWMAX transmit success"
        elif moveCommand == "JAWMIN":
            issueCommand("MOVEJAWMIN")
            return "MOVEJAWMIN transmit success"
        elif moveCommand == "JAWCENTER":
            issueCommand("MOVEJAWCENTER")
            return "MOVEJAWCENTER transmit success"
        elif moveCommand == "JAWNUDGEUP":
            issueCommand("MOVEJAWNUDGEUP")
            return "MOVEJAWNUDGEUP transmit success"
        elif moveCommand == "JAWNUDGEDOWN":
            issueCommand("MOVEJAWNUDGEDOWN")
            return "MOVEJAWNUDGEDOWN transmit success"
        elif moveCommand == "EYESVMAX":
            issueCommand("MOVEEYESVMAX")
            return "MOVEEYESVMAX transmit success"
        elif moveCommand == "EYESVMIN":
            issueCommand("MOVEEYESVMIN")
            return "MOVEEYESVMIN transmit success"
        elif moveCommand == "EYESVCENTER":
            issueCommand("MOVEEYESVCENTER")
            return "MOVEEYESVCENTER transmit success"
        elif moveCommand == "EYESVNUDGEUP":
            issueCommand("MOVEEYESVNUDGEUP")
            return "MOVEEYESVNUDGEUP transmit success"
        elif moveCommand == "EYESVNUDGEDOWN":
            issueCommand("MOVEEYESVNUDGEDOWN")
            return "MOVEEYESVNUDGEDOWN transmit success"
        elif moveCommand == "EYESHMAX":
            issueCommand("MOVEEYESHMAX")
            return "MOVEEYESHMAX transmit success"
        elif moveCommand == "EYESHMIN":
            issueCommand("MOVEEYESHMIN")
            return "MOVEEYESHMIN transmit success"
        elif moveCommand == "EYESHCENTER":
            issueCommand("MOVEEYESHCENTER")
            return "MOVEEYESHCENTER transmit success"
        elif moveCommand == "EYESHNUDGEUP":
            issueCommand("MOVEEYESHNUDGEUP")
            return "MOVEEYESHNUDGEUP transmit success"
        elif moveCommand == "EYESHNUDGEDOWN":
            issueCommand("MOVEEYESHNUDGEDOWN")
            return "MOVEEYESHNUDGEDOWN transmit success"
        elif moveCommand == "NECKPIVOTMAX":
            issueCommand("MOVENECKPIVOTMAX")
            return "MOVENECKPIVOTMAX transmit success"
        elif moveCommand == "NECKPIVOTMIN":
            issueCommand("MOVENECKPIVOTMIN")
            return "MOVENECKPIVOTMIN transmit success"
        elif moveCommand == "NECKPIVOTCENTER":
            issueCommand("MOVENECKPIVOTCENTER")
            return "MOVENECKPIVOTCENTER transmit success"
        elif moveCommand == "NECKPIVOTNUDGEUP":
            issueCommand("MOVENECKPIVOTNUDGEUP")
            return "MOVENECKPIVOTNUDGEUP transmit success"
        elif moveCommand == "NECKPIVOTNUDGEDOWN":
            issueCommand("MOVENECKPIVOTNUDGEDOWN")
            return "MOVENECKPIVOTNUDGEDOWN transmit success"
        else:
            return "MOVE COMMAND NOT RECOGNIZED!"
        
    @app.route('/SET/<setCommand>')
    def setCommand(setCommand):

        if setCommand == "JAWMAX":
            issueCommand("SETJAWMAX")
            return "SETJAWMAX transmit success"
        elif setCommand == "JAWMIN":
            issueCommand("SETJAWMIN")
            return "SETJAWMIN transmit success"
        elif setCommand == "JAWCENTER":
            issueCommand("SETJAWCENTER")
            return "SETJAWCENTER transmit success"
        elif setCommand == "EYESVMAX":
            issueCommand("SETEYESVMAX")
            return "SETEYESVMAX transmit success"
        elif setCommand == "EYESVMIN":
            issueCommand("SETEYESVMIN")
            return "SETEYESVMIN transmit success"
        elif setCommand == "EYESVCENTER":
            issueCommand("SETEYESVCENTER")
            return "SETEYESVCENTER transmit success"
        elif setCommand == "EYESHMAX":
            issueCommand("SETEYESHMAX")
            return "SETEYESHMAX transmit success"
        elif setCommand == "EYESHMIN":
            issueCommand("SETEYESHMIN")
            return "SETEYESHMIN transmit success"
        elif setCommand == "EYESHCENTER":
            issueCommand("SETEYESHCENTER")
            return "SETEYESHCENTER transmit success"
        elif setCommand == "NECKPIVOTMAX":
            issueCommand("SETNECKPIVOTMAX")
            return "SETNECKPIVOTMAX transmit success"
        elif setCommand == "NECKPIVOTMIN":
            issueCommand("SETNECKPIVOTMIN")
            return "SETNECKPIVOTMIN transmit success"
        elif setCommand == "NECKPIVOTCENTER":
            issueCommand("SETNECKPIVOTCENTER")
            return "SETNECKPIVOTCENTER transmit success"
        else:
            return "SET COMMAND NOT RECOGNIZED!"

    def issueCommand(command):

        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        dtg = datetime.datetime.now()

        dateString = dtg.strftime("%Y-%m-%d")
        timeString = dtg.strftime("%H:%M:%S")
        insertStatement = "INSERT INTO outbound(commandMessage,currentDate,currentTime, processed) VALUES(?,?,?,?)"
        dataValues = [command,dateString,timeString, 0]
        cur.execute(insertStatement, dataValues)
        con.commit()
        con.close()

    return app



API = headControllerAPI()

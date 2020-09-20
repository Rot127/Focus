#!/usr/bin/env python3

import argparse
import time, os, random
import datetime as dt

class Focus:

    flowTime = 90 * 60 # Timer for flow phase in seconds
    flowOvertime = 15 * 60 # The minutes which are given gratefully to the user if she is in the flow.
    planTime = 45 * 60 # Timer for plan phase in seconds
    breakTime = 20 * 60 # Minimum time of a break

    emptyInfo = { "title":"EMPTY TITLE", "timer":0, "info":"" }
    info = emptyInfo

    questions = list()

    def __init__(self, pathToQuestionFile, workTime, breakTime, overtime):
        self.flowTime = workTime if workTime > 0 else 90 * 60
        self.flowOvertime = overtime if overtime > 0 else 15 * 60
        self.planTime = workTime if workTime > 0 else 45 * 60
        self.breakTime = breakTime if breakTime > 0 else 20 * 60

        try:
            for question in open(pathToQuestionFile, "r"):
                self.questions.append(question)
        except Exception as e:
            print(e)
            exit(1)

    def runTimer(self, planTime):
        currTime = planTime
        while currTime > 0:
            self.info["timer"] = currTime
            self.printInfoToCmd()
            time.sleep(1)
            currTime -= 1

    def enterPlanPhase(self):
        self.info["title"] = "PLANNING TIMER"
        self.runTimer(self.planTime)
        self.annoyUser()
        self.enterBreakTime()
        self.printQuestions()
        return

    def enterFlowPhase(self):
        self.info["title"] = "FLOW TIMER"
        time = self.flowTime

        inFlow = True
        while inFlow:
            self.runTimer(time)
            self.annoyUser()
            inFlow = self.askForExtension()
            time = self.flowOvertime
            self.info["info"] = ""

        self.enterBreakTime()
        self.printQuestions()
        return

    def enterBreakTime(self):
        print("-> Go! Make a break.")
        self.info["title"] = "BREAK TIME"
        self.info["info"] = ""
        self.runTimer(self.breakTime)

    def printQuestions(self):
        answer = "n"
        while answer == "n":
            qi = random.randint(0, len(self.questions))
            q = self.questions[qi]
            print("QUESTION: {}".format(q))
            answer = input("Next question [n] or continue [any] > ")

    def askForExtension(self):
        answer = ""
        while answer != "y" or answer != "no":
            answer = input("Do you need some overtime? [y/n] > ")
            if answer == "y":
                return True
            elif answer == "n":
                return False
            else:
                print("Please only type 'y' or 'n'")

    def printInfoToCmd(self):
        info = self.info

        ty_res = time.gmtime(info["timer"])
        res = time.strftime("%H:%M:%S", ty_res)
        absolutely_unused_variable = os.system("clear")
        print(info["title"])
        if info["timer"] >= 0:
            print(res)
        print(info["info"])

    def annoyUser(self):
        self.info["info"] = "TIME UP!"
        self.printInfoToCmd()
        sendNoticeToOS()

    def resetScreenOutput(self):
        self.info = self.emptyInfo


def sendNoticeToOS():
        command = "notify-send 'Timer up!' --icon=clock"
        os.system(command)

parser = argparse.ArgumentParser(description="Break reminder")
parser.add_argument("-m", dest="timerMode", action="store", metavar="t",
                    required=True, choices = ["f", "p"],
                    help="Mode of timer. Flow mode (f) or planning mode (p)")

parser.add_argument("-p", dest="path", action="store", default="",
                    help="Path to the question file")

parser.add_argument('-t', metavar='n', type=int, dest="duration", default=0,
                    help='Duration of work timer in minutes')

parser.add_argument('-o', metavar='n', type=int, dest="overtime", default=0,
                    help='Overtime for the flow mode in minutes')

parser.add_argument('-b', metavar='n', type=int, dest="breakLength", default=0,
                    help='Duration of break in minutes')

if __name__ == "__main__":
    args = parser.parse_args()
    duration = args.duration * 60
    overtime = args.overtime * 60
    breakLength = args.breakLength * 60
    path = args.path if args.path != "" else "./questions_EN"

    timerMode = args.timerMode
    foc = Focus(path, duration, breakLength, overtime)
    if timerMode == "f":
        foc.enterFlowPhase()
    elif timerMode == "p":
        foc.enterPlanPhase()


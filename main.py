

import numpy as np
import random
import RPi.GPIO as GPIO
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import sys
import time


GPIO.setmode(GPIO.BCM)

# set GPIO Pins

GPIO_TRIGGER1 = 2
GPIO_TRIGGER2 = 3
GPIO_TRIGGER3 = 1
GPIO_ECHO1 = 14
GPIO_ECHO2 = 15
GPIO_ECHO3 = 7
    #
# Initialization functions

GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)


# Classes


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def checkPos(pos1, pos2):
        if (pos1.x == pos2.x) and (pos1.y == pos2.y):
            return True
        return False

    def copyPos(self, pos):
        self.x = pos.x
        self.y = pos.y


class Queue:

    def __init__(self):
        self.queue = list()

    def addtoq(self, dataval):
        if dataval not in self.queue:
            self.queue.insert(0, dataval)
            return True
        return False

    def removefromq(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return ("No elements in Queue!")

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

#    def printstack(self):
#        for i in range(0, self.size()):
#            print(self.items[i].value, end = " ")
#        print(" ")

    def copy(self, cp):
        for i in range(0, cp.size()):
            self.push(cp.items[i])

    def add(self, cp):

        temp = Stack()

        for j in range(0, self.size()):
            temp.push(self.items[j])
        for i in range(0, cp.size()):
            temp.push(cp.items[i])

        self.copy(temp)


class Node(Position):

    def __init__(self, value, pos, wall1, wall2, wall3, wall4, orientationPriority, visited, ignore, colorBlock,
                 qrBlock, build):
        Position.__init__(self, pos.x, pos.y)
        self.value = value
        self.pos = pos
        self.wall1 = wall1
        self.wall2 = wall2
        self.wall3 = wall3
        self.wall4 = wall4
        self.orientationPriority = orientationPriority
        self.visited = visited
        self.ignore = ignore
        self.colorBlock = colorBlock
        self.qrBlock = qrBlock
        self.build = build

    def printNode(self):
        print("Value: {}".format(self.value))
        print("Pos: {} {}".format(self.pos.x, self.pos.y))
        print("Wall: {} {} {} {}".format(self.wall1, self.wall2, self.wall3, self.wall4))
        print("O Priority: {}".format(self.orientationPriority))
        print("Visited: {}".format(self.visited))
        print("Ignore: {}".format(self.ignore))
        print("C Block: {}".format(self.colorBlock))
        print("Build: {}".format(self.build))


class Bot:

    def __init__(self, pos, orientation):
        self.pos = pos
        self.orientation = orientation  # 1 - north, 2 - east, 3 - south, 4 - west

    def move(self, newPos, newOrientation):
        self.pos = newPos
        self.orientation = newOrientation


# global variables

startPos = Position(0, 0)
block1 = Position(0, 7)
block2 = Position(3, 2)
block3 = Position(5, 1)
qrBLock1 = Position(4, 4)
qrBLock2 = Position(8, 6)
endPos = Position(8, 0)

blockCount1 = 0
blockCount2 = 0

botPos = Position(0, 0)
botOrientation = 1
bot = Bot(botPos, botOrientation)

# adi's international(halli) code

# GPIO Mode (BOARD / BCM)

#GPIO.setmode(GPIO.BCM)
#
## set GPIO Pins
#
#GPIO_TRIGGER1 = 2
#GPIO_TRIGGER2 = 3
#GPIO_TRIGGER3 = 1
#GPIO_ECHO1 = 14
#GPIO_ECHO2 = 15
#GPIO_ECHO3 = 7
#    #
## Initialization functions
#
#GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
#GPIO.setup(GPIO_ECHO1, GPIO.IN)
#GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
#GPIO.setup(GPIO_ECHO2, GPIO.IN)
#GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
#GPIO.setup(GPIO_ECHO3, GPIO.IN)


def distance(num):
    GPIO.setmode(GPIO.BCM)

# set GPIO Pins

    GPIO_TRIGGER1 = 2
    GPIO_TRIGGER2 = 3
    GPIO_TRIGGER3 = 1
    GPIO_ECHO1 = 14
    GPIO_ECHO2 = 15
    GPIO_ECHO3 = 7
        #
    # Initialization functions
    
    GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
    GPIO.setup(GPIO_ECHO1, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
    GPIO.setup(GPIO_ECHO2, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
    GPIO.setup(GPIO_ECHO3, GPIO.IN)
    # set Trigger to HIGH
    
    if num == 1:
        GPIO.output(GPIO_TRIGGER1, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.1)
        GPIO.output(GPIO_TRIGGER1, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO1) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO1) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

    if num == 2:
        GPIO.output(GPIO_TRIGGER2, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.1)
        GPIO.output(GPIO_TRIGGER2, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO2) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO2) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

    if num == 3:
        GPIO.output(GPIO_TRIGGER3, True)
 
    # set Trigger after 0.01ms to LOW
        time.sleep(1)
        GPIO.output(GPIO_TRIGGER3, False)
 
        StartTime = time.time()
        StopTime = time.time()
 
    # save StartTime
        while GPIO.input(GPIO_ECHO3) == 0:
            StartTime = time.time()
 
    # save time of arrival
        while GPIO.input(GPIO_ECHO3) == 1:
            StopTime = time.time()
 
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        
        

        print("caught ", distance)

    return distance


# motor functions

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)


def forward(tf):
    init()
    GPIO.output(9, False)
    GPIO.output(25, False)
    GPIO.output(5, False)
    GPIO.output(12, False)
    GPIO.output(10, True)
    GPIO.output(8, True)
    GPIO.output(6, True)
    GPIO.output(13, True)

    time.sleep(tf)
    GPIO.cleanup()


def reverse(tf):
    init()
    GPIO.output(9, True)
    GPIO.output(25, True)
    GPIO.output(5, True)
    GPIO.output(12, True)
    GPIO.output(10, False)
    GPIO.output(8, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    time.sleep(tf)

    GPIO.cleanup()


def right(tf):
    init()

    GPIO.output(9, False)
    GPIO.output(10, True)
    GPIO.output(25, False)
    GPIO.output(8, True)
    time.sleep(tf)

    GPIO.cleanup()


def left(tf):
    init()
    GPIO.output(9, True)
    GPIO.output(10, False)
    GPIO.output(25, True)
    GPIO.output(8, False)
    GPIO.output(5, False)
    GPIO.output(6, True)
    GPIO.output(12, False)
    GPIO.output(13, True)
    time.sleep(tf)
    GPIO.cleanup()


# sensor functions

def wallADetected():  # left ultrasonic
    
    left_wall = distance(3)
    print(distance)

    if left_wall <= 5:
        return True
    return False


def wallBDetected():  # front ultrasonic
    front_wall = distance(2)

    if front_wall <= 5.5:
        return True
    return False


def wallCDetected():  # right ultrasonic
    right_wall = distance(1)

    if right_wall <= 5:
        return True
    return False


def colorBlockDetected():
    return False


def qrCodeScanned():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                    help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")

    # vs = VideoStream(src=0).start()
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open(args["output"], "w")
    found = set()

    # loop over the frames from the video stream
    for i in range(0, 10):
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # OpenCV barcode and QR code scanner with ZBarPython

        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            print(text)

            str(text)
            if text == "1" or text == "2" or text == "3" or text == "4":
                return True

            # if the barcode text is currently not in our CSV file, write
            # the timestamp + barcode to disk and update the set
            if barcodeData not in found:
                csv.write("{},{}\n".format(datetime.datetime.now(),
                                           barcodeData))
                csv.flush()
                found.add(barcodeData)

        # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # close the output CSV file do a bit of cleanup
    print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()

    return False


# matrix functions


def copyMatrix(m1, m2):
    for i in range(0, 9):
        for j in range(0, 9):
            m1[i][j] = m2[i][j]


def defaultMatrix():
    defMaze = np.empty((9, 9), dtype=object)

    # Ignore the following blocks
    for i in range(0, 9):
        if i == 4:
            defMaze[4][4] = Node(0, Position(4, 4), True, False, True, False, 0, False, False, False,
                                 True, False)  # qr code block
            continue
        defMaze[4][i] = Node(None, Position(4, i), True, True, True, True, 0, False, True, False, False, False)

    count1 = 1
    count2 = 2
    pos1 = Position(3, 4)
    pos2 = Position(5, 4)
    pos1a = Position(3, 4)
    pos2a = Position(5, 4)

    for i in range(4):

        defMaze[pos1.x][pos1.y] = Node(count1, Position(pos1.x, pos1.y), False, False, False, False, 0, False, False,
                                       False, False, False)
        defMaze[pos2.x][pos2.y] = Node(count1, Position(pos2.x, pos2.y), False, False, False, False, 0, False, False,
                                       False, False, False)
        count2 = count1
        for j in range(5):
            defMaze[pos1.x][pos1.y] = Node(count2, Position(pos1.x, pos1.y), False, False, False, False, 0, False,
                                           False, False, False, False)
            defMaze[pos2.x][pos2.y] = Node(count2, Position(pos2.x, pos2.y), False, False, False, False, 0, False,
                                           False, False, False, False)
            defMaze[pos1a.x][pos1a.y] = Node(count2, Position(pos1a.x, pos1a.y), False, False, False, False, 0, False,
                                             False, False, False, False)
            defMaze[pos2a.x][pos2a.y] = Node(count2, Position(pos2a.x, pos2a.y), False, False, False, False, 0, False,
                                             False, False, False, False)
            pos1.y = pos1.y + 1
            pos2.y = pos2.y + 1
            pos1a.y = pos1a.y - 1
            pos2a.y = pos2a.y - 1
            count2 = count2 + 1
        pos1.x = pos1.x - 1
        pos2.x = pos2.x + 1
        pos1a.x = pos1a.x - 1
        pos2a.x = pos2a.x + 1
        pos1.y = 4
        pos2.y = 4
        pos1a.y = 4
        pos2a.y = 4
        count1 = count1 + 1

    for a in range(0, 9):
        defMaze[a][8].wall1 = True

    for b in range(0, 9):
        defMaze[b][0].wall3 = True

    for c in range(0, 9):
        defMaze[0][c].wall4 = True

    for d in range(0, 9):
        defMaze[8][d].wall2 = True

    return defMaze


def buildMatrix(dest, set):
    newMaze = np.empty((9, 9), dtype=object)
    newMaze = defaultMatrix()
    s = Queue()
    count = 0
    pos = Position(dest.x, dest.y)
    currentNode = Node(0, pos, False, False, False, False, 0, False, False, False, False, True)
    s.addtoq(currentNode)

    currentNodeStack = Stack()

    if set == 1:
        for i in range(5, 9):
            for j in range(0, 9):
                newMaze[i][j] = Node(None, Position(i, j), True, True, True, True, 0, False, True, False, False, True)
        newMaze[dest.x][dest.y] = currentNode

        for i in range(0, 11):
            while not (s.size() == 0):
                currentNode = s.removefromq()
                pos = currentNode.pos
                openNeighbourStack = Stack()
                openNeighbourStack = getOpenNeighbour(newMaze, pos)
                currentNodeStack.add(openNeighbourStack)

            while not (currentNodeStack.size() == 0):
                neighbourNode = currentNodeStack.pop()

                if not neighbourNode.build:
                    neighbourNode.value = currentNode.value + 1
                    neighbourNode.build = True
                    s.addtoq(neighbourNode)

    if set == 2:
        currentNode = Node(0, pos, False, False, False, False, 0, False, False, False, False, True)
        for i in range(0, 4):
            for j in range(0, 9):
                newMaze[i][j] = Node(None, Position(i, j), True, True, True, True, 0, False, True, False, False, True)
        newMaze[dest.x][dest.y] = currentNode

        for i in range(0, 11):
            while not (s.size() == 0):
                currentNode = s.removefromq()
                pos = currentNode.pos
                openNeighbourStack = Stack()
                openNeighbourStack = getOpenNeighbour(newMaze, pos)
                currentNodeStack.add(openNeighbourStack)

            while not (currentNodeStack.size() == 0):
                neighbourNode = currentNodeStack.pop()

                if not neighbourNode.build:
                    neighbourNode.value = currentNode.value + 1
                    neighbourNode.build = True
                    s.addtoq(neighbourNode)

    if set == 3:
        currentNode = Node(0, pos, False, False, False, False, 0, False, False, False, False, True)
        for i in range(0, 9):
            if i == 4:
                newMaze[4][4] = Node(0, Position(4, 4), True, False, True, False, 0, False, False, False,
                                     True, False)  # qr code block
                continue
            newMaze[4][i] = Node(None, Position(4, i), True, True, True, True, 0, False, True, False, False, False)
        newMaze[dest.x][dest.y] = currentNode

        for i in range(0, 16):
            while not (s.size() == 0):
                currentNode = s.removefromq()
                pos = currentNode.pos
                openNeighbourStack = Stack()
                openNeighbourStack = getOpenNeighbour(newMaze, pos)
                currentNodeStack.add(openNeighbourStack)

            while not (currentNodeStack.size() == 0):
                neighbourNode = currentNodeStack.pop()

                if not neighbourNode.build:
                    neighbourNode.value = currentNode.value + 1
                    neighbourNode.build = True
                    s.addtoq(neighbourNode)

    return newMaze


def printMaze(mazeValue, botValue):
    x = 0
    y = 8

    while y >= 0:
        for i in range(0, 9):
            if mazeValue[i][y].wall1:
                print("{}{}{}".format(" ", "-", " "), end=" ")
            else:
                print("{}{}{}".format(" ", " ", " "), end=" ")
        print("")
        while x <= 8:
            if mazeValue[x][y] is None:
                print("{}{}{}".format(" ", "!", " "), end="")
            elif Position.checkPos(mazeValue[x][y].pos, botValue.pos):
                if botValue.orientation == 1:
                    if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                        print("{}{}{}".format("|", "A", "|"), end="")
                    elif mazeValue[x][y].wall2:
                        print("{}{}{}".format(" ", "A", "|"), end="")
                    elif mazeValue[x][y].wall4:
                        print("{}{}{}".format("|", "A", " "), end="")
                    else:
                        print("{}{}{}".format(" ", "A", " "), end="")
                elif botValue.orientation == 2:
                    if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                        print("{}{}{}".format("|", ">", "|"), end="")
                    elif mazeValue[x][y].wall2:
                        print("{}{}{}".format(" ", ">", "|"), end="")
                    elif mazeValue[x][y].wall4:
                        print("{}{}{}".format("|", ">", " "), end="")
                    else:
                        print("{}{}{}".format(" ", ">", " "), end="")
                elif botValue.orientation == 3:
                    if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                        print("{}{}{}".format("|", "V", "|"), end="")
                    elif mazeValue[x][y].wall2:
                        print("{}{}{}".format(" ", "V", "|"), end="")
                    elif mazeValue[x][y].wall4:
                        print("{}{}{}".format("|", "V", " "), end="")
                    else:
                        print("{}{}{}".format(" ", "V", " "), end="")
                elif botValue.orientation == 4:
                    if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                        print("{}{}{}".format("|", "<", "|"), end="")
                    elif mazeValue[x][y].wall2:
                        print("{}{}{}".format(" ", "<", "|"), end="")
                    elif mazeValue[x][y].wall4:
                        print("{}{}{}".format("|", "<", " "), end="")
                    else:
                        print("{}{}{}".format(" ", "<", " "), end="")
                else:
                    if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                        print("{}{}{}".format("|", "T", "|"), end="")
                    elif mazeValue[x][y].wall2:
                        print("{}{}{}".format(" ", "T", "|"), end="")
                    elif mazeValue[x][y].wall4:
                        print("{}{}{}".format("|", "T", " "), end="")
                    else:
                        print("{}{}{}".format(" ", "T", " "), end="")
            elif mazeValue[x][y].ignore:
                if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                    print("{}{}{}".format("|", "X", "|"), end="")
                elif mazeValue[x][y].wall2:
                    print("{}{}{}".format(" ", "X", "|"), end="")
                elif mazeValue[x][y].wall4:
                    print("{}{}{}".format("|", "X", " "), end="")
                else:
                    print("{}{}{}".format(" ", "X", " "), end="")
            else:
                if mazeValue[x][y].wall4 and mazeValue[x][y].wall2:
                    print("{}{}{}".format("|", mazeValue[x][y].value, "|"), end="")
                elif mazeValue[x][y].wall2:
                    print("{}{}{}".format(" ", mazeValue[x][y].value, "|"), end="")
                elif mazeValue[x][y].wall4:
                    print("{}{}{}".format("|", mazeValue[x][y].value, " "), end="")
                else:
                    print("{}{}{}".format(" ", mazeValue[x][y].value, " "), end="")
            x = x + 1
        if y == 0:
            print("")
        for j in range(0, 9):
            if mazeValue[i][y].wall3:
                print("{}{}{}".format(" ", "-", " "), end="")
            else:
                print("{}{}{}".format(" ", " ", " "), end="")
        y = y - 1
        x = 0
        print("")


# algorithm functions

def getOpenNeighbour(mazeMap, botPos):
    s = Stack()
    x = botPos.x
    y = botPos.y

    if (not y >= 8) and (not mazeMap[x][y + 1].wall3):  # upblock
        mazeMap[x][y + 1].orientationPriority = 1
        s.push(mazeMap[x][y + 1])
    if (not x >= 8) and (not mazeMap[x + 1][y].wall4):  # rightblock
        mazeMap[x + 1][y].orientationPriority = 2
        s.push(mazeMap[x + 1][y])
    if (not y <= 0) and (not mazeMap[x][y - 1].wall1):  # downblock
        mazeMap[x][y - 1].orientationPriority = 3
        s.push(mazeMap[x][y - 1])
    if (not x <= 0) and (not mazeMap[x - 1][y].wall2):  # leftblock
        mazeMap[x - 1][y].orientationPriority = 4
        s.push(mazeMap[x - 1][y])
    if s.size() == 0:
        print("No open neighbours")
    return s


def getMinOpenNeighbour(openNeighbourStack, botInfo):
    currentNode = Node(0, Position(0, 0), False, False, False, False, 0, False, False, False, False, False)
    s = Stack()
    cp = Stack()
    cp.copy(openNeighbourStack)
    smallestValue = 100
    for i in range(0, openNeighbourStack.size()):
        currentNode = openNeighbourStack.pop()
        if currentNode.value <= smallestValue:
            smallestValue = currentNode.value
    for k in range(0, cp.size()):
        curValue = cp.pop()
        if curValue.value == smallestValue:
            s.push(curValue)
    cp2 = Stack()
    cp2.copy(s)
    if s.size() == 0:
        print("No min open neighbour")
        exit()
    if not s.size() == 1:
        for j in range(0, s.size()):
            currentNode = s.pop()
            if currentNode.orientationPriority == botInfo.orientation:
                return currentNode
        for k in range(0, cp2.size()):
            currentNode = cp2.pop()
            if botInfo.orientation % 2 == 1:
                if currentNode.orientationPriority % 2 == 0:
                    return currentNode
            if botInfo.orientation % 2 == 0:
                if currentNode.orientationPriority % 2 == 1:
                    return currentNode

    return s.pop()


def getOrientation(currentPos, futurePos):
    x1 = currentPos.x
    y1 = currentPos.y
    x2 = futurePos.x
    y2 = futurePos.y

    if (x2 == x1) and (y2 == y1 + 1):
        return 1
    if (x2 == x1 + 1) and (y2 == y1):
        return 2
    if (x2 == x1) and (y2 == y1 - 1):
        return 3
    if (x2 == x1 - 1) and (y2 == y1):
        return 4

    return 0


def updateWalls(map, bot):
    x = bot.pos.x
    y = bot.pos.y
    o = bot.orientation

    a = wallADetected()
    b = wallBDetected()
    c = wallCDetected()

    if not (a or b or c):
        return False

    if o == 1:

        if a:
            map[x][y].wall4 = True
            if not x <= 0:
                map[x - 1][y].wall2 = True
        if b:
            map[x][y].wall1 = True
            if not y >= 8:
                map[x][y + 1].wall3 = True
        if c:
            map[x][y].wall2 = True
            if not x >= 8:
                map[x + 1][y].wall4 = True

    elif o == 2:

        if a:
            map[x][y].wall1 = True
            if not y >= 8:
                map[x][y + 1].wall3 = True
        if b:
            map[x][y].wall2 = True
            if not x >= 8:
                map[x + 1][y].wall4 = True
        if c:
            map[x][y].wall3 = True
            if not y <= 0:
                map[x][y - 1].wall1 = True

    elif o == 3:

        if a:
            map[x][y].wall2 = True
            if not x >= 8:
                map[x + 1][y].wall4 = True
        if b:
            map[x][y].wall3 = True
            if not y <= 0:
                map[x][y - 1].wall1 = True
        if c:
            map[x][y].wall4 = True
            if not x <= 0:
                map[x - 1][y].wall2 = True

    elif o == 4:

        if a:
            map[x][y].wall3 = True
            if not y <= 0:
                map[x][y - 1].wall1 = True
        if b:
            map[x][y].wall1 = True
            if not x <= 0:
                map[x - 1][y].wall3 = True
        if c:
            map[x][y].wall2 = True
            if not y >= 8:
                map[x][y + 1].wall4 = True

    else:

        return False

    return True


def changeOrientation(finalOrientation):
    print(bot.orientation, " ", finalOrientation)
    if bot.orientation == 1:
        if finalOrientation == 1:
            return 0
        if finalOrientation == 2:
            right(2)  # 90 degrees
        if finalOrientation == 3:
            right(1)  # 180 degrees
        if finalOrientation == 4:
            left(2)  # - 90 degrees
    if bot.orientation == 2:
        if finalOrientation == 1:
            left(2)  # - 90 degrees
        if finalOrientation == 2:
            return 0
        if finalOrientation == 3:
            right(2)  # 90 degrees
        if finalOrientation == 4:
            right(1)  # 180 degrees
    if bot.orientation == 3:
        if finalOrientation == 1:
            right(1)  # 180 degrees
        if finalOrientation == 2:
            left(2)  # - 90 degrees
        if finalOrientation == 3:
            return 0
        if finalOrientation == 4:
            right(2)  # 90 degrees
    if bot.orientation == 4:
        if finalOrientation == 1:
            right(2)  # 90 degrees
        if finalOrientation == 2:
            right(1)  # 180 degrees
        if finalOrientation == 3:
            left(2)  # - 90 degrees
        if finalOrientation == 4:
            return 0


def turnEnginesOn():
    forward(2)


def moveToLowerValue(map):
    openNeighbour = getOpenNeighbour(map, bot.pos)  # dumps em frickin open neighbours in a stack
    minOpenNeighbour = getMinOpenNeighbour(openNeighbour, bot)  # finds the minimum open neighbour from the stack
    orientation = getOrientation(bot.pos, minOpenNeighbour.pos)  # finds the new orientation of the bot
    bot.move(minOpenNeighbour.pos, orientation)  # move the bot to the new node
    changeOrientation(orientation)
    turnEnginesOn()


def botMove(dest, map):
    while not Position.checkPos(dest, bot.pos):
        moveToLowerValue(map)
        printMaze(map, bot)
        time.sleep(0.5)


def floodFillAlgorithm(map):
    if updateWalls(map, bot):
        floodStack = Stack()
        currentNode = Node(0, Position(0, 0), False, False, False, False, 0, False, False, False, False, False)
        floodStack.push(map[bot.pos.x, bot.pos.y])
        while not (floodStack.size() == 0):
            currentNode = floodStack.pop()
            openNeighbourStack = Stack()
            openNeighbourStack = getOpenNeighbour(map, bot.pos)
            minNb = Node(0, Position(0, 0), False, False, False, False, 0, False, False, False, False, False)
            minNb = getMinOpenNeighbour(openNeighbourStack, bot)
            if currentNode.value == (minNb.value + 1):
                continue
            currentNode.value = minNb.value + 1
            while not (openNeighbourStack.size() == 0):
                floodStack.push(openNeighbourStack.pop())


def floodFill(dest, map):
    while not Position.checkPos(bot.pos, dest):

        if colorBlockDetected():
            while colorBlockDetected():
                time.sleep(1)

        if qrCodeScanned():
            while qrCodeScanned():
                time.sleep(1)

        floodFillAlgorithm(map)
        # moves to lower value
        moveToLowerValue(map)
        printMaze(map, bot)
        print("")
        time.sleep(0.5)


def floodFillForExploreX(dest, mapX):
    while not Position.checkPos(bot.pos, dest):

        if colorBlockDetected():
            blockCount1 = blockCount1 + 1;
            if blockCount1 == 1:
                if bot.orientation == 1:
                    block1.x = bot.pos.x
                    block1.y = bot.pos.y + 1
                if bot.orientation == 2:
                    block1.x = bot.pos.x + 1
                    block1.y = bot.pos.y
                if bot.orientation == 3:
                    block1.x = bot.pos.x
                    block1.y = bot.pos.y - 1
                if bot.orientation == 4:
                    block1.x = bot.pos.x - 1
                    block1.y = bot.pos.y
            if blockCount1 == 2:
                if bot.orientation == 1:
                    block2.x = bot.pos.x
                    block2.y = bot.pos.y + 1
                if bot.orientation == 2:
                    block2.x = bot.pos.x + 1
                    block2.y = bot.pos.y
                if bot.orientation == 3:
                    block2.x = bot.pos.x
                    block2.y = bot.pos.y - 1
                if bot.orientation == 4:
                    block2.x = bot.pos.x - 1
                    block2.y = bot.pos.y
            while colorBlockDetected():
                time.sleep(1)

        if qrCodeScanned():
            while qrCodeScanned():
                time.sleep(1)

        floodFillAlgorithm(mapX)
        # moves to lower value
        moveToLowerValue(mapX)
        printMaze(mapX, bot)
        print("")
        time.sleep(0.5)


def floodFillForExploreY(dest, mapY):
    while not Position.checkPos(bot.pos, dest):

        if colorBlockDetected():
            if bot.orientation == 1:
                block3.x = bot.pos.x
                block3.y = bot.pos.y + 1
            if bot.orientation == 2:
                block3.x = bot.pos.x + 1
                block3.y = bot.pos.y
            if bot.orientation == 3:
                block3.x = bot.pos.x
                block3.y = bot.pos.y - 1
            if bot.orientation == 4:
                block3.x = bot.pos.x - 1
                block3.y = bot.pos.y
            while colorBlockDetected():
                time.sleep(1)

        if qrCodeScanned():
            if bot.orientation == 1:
                qrBLock2.x = bot.pos.x
                qrBLock2.y = bot.pos.y + 1
            if bot.orientation == 2:
                qrBLock2.x = bot.pos.x + 1
                qrBLock2.y = bot.pos.y
            if bot.orientation == 3:
                qrBLock2.x = bot.pos.x
                qrBLock2.y = bot.pos.y - 1
            if bot.orientation == 4:
                qrBLock2.x = bot.pos.x - 1
                qrBLock2.y = bot.pos.y
            while qrCodeScanned():
                time.sleep(1)

        floodFillAlgorithm(mapY)
        # moves to lower value
        moveToLowerValue(mapY)
        printMaze(mapY, bot)
        print("")
        time.sleep(0.5)


def generatePos(xmin, xmax, ymin, ymax):
    pos = Position(0, 0)
    pos.x = random.randint(xmin, xmax)
    pos.y = random.randint(ymin, ymax)
    return pos


def exploreMapX():
    p = Position(0, 1)

    for i in range(0, 8):

        map = buildMatrix(p, 1)
        # printMaze(map, bot)

        if blockCount1 == 2:
            return 0

        floodFillForExploreX(p, map)

        p.y = p.y + 1

    p = Position(1, 8)

    for i in range(0, 3):

        map = buildMatrix(p, 1)
        # printMaze(map, bot)

        if blockCount1 == 2:
            return 0

        floodFillForExploreX(p, map)

        p.x = p.x + 1

    p = Position(3, 7)

    for i in range(0, 8):

        map = buildMatrix(p, 1)
        # printMaze(map, bot)

        if blockCount1 == 2:
            return 0

        floodFillForExploreX(p, map)

        p.y = p.y - 1

    p = Position(2, 0)

    for i in range(0, 3):

        map = buildMatrix(p, 1)
        # printMaze(map, bot)

        if blockCount1 == 2:
            return 0

        floodFillForExploreX(p, map)

        p.x = p.x - 1


def exploreMapY():
    p = Position(5, 5)

    for i in range(0, 3):

        map = buildMatrix(p, 2)

        if blockCount2 == 2:
            return 0

        floodFillForExploreY(p, map)

        p.y = p.y + 1

    p = Position(6, 8)

    for i in range(0, 3):

        map = buildMatrix(p, 2)

        if blockCount2 == 2:
            return 0

        floodFillForExploreY(p, map)

        p.x = p.x + 1

    p = Position(8, 7)

    for i in range(0, 8):

        map = buildMatrix(p, 2)

        if blockCount2 == 2:
            return 0

        floodFillForExploreY(p, map)

        p.y = p.y - 1

    p = Position(7, 0)

    for i in range(0, 3):

        map = buildMatrix(p, 2)

        if blockCount2 == 2:
            return 0

        floodFillForExploreY(p, map)

        p.x = p.x - 1

    p = Position(5, 1)

    for i in range(0, 3):

        map = buildMatrix(p, 2)

        if blockCount2 == 2:
            return 0

        floodFillForExploreY(p, map)

        p.y = p.y + 1


def gotoY():
    map = np.empty((9, 9), dtype=object)
    dest = Position(5, 4)
    map = buildMatrix(dest, 1)
    p = Position(4, 4)
    map[4][4] = Node(0, p, False, False, False, False, 0, False, False, False, False, False)
    p = Position(5, 4)
    map[5][4] = Node(1, p, False, False, False, False, 0, False, False, False, False, False)
    bot.orientation = 1
    bot.x = 0
    bot.y = 0
    floodFill(dest, map)


def gotoX():
    map = np.empty((9, 9), dtype=object)
    dest = Position(0, 0)
    map = buildMatrix(dest, 3)
    floodFill(dest, map)


# The start of the program

map1 = np.empty((9, 9), dtype=object)
map2 = np.empty((9, 9), dtype=object)
map3 = np.empty((9, 9), dtype=object)
map4 = np.empty((9, 9), dtype=object)
map5 = np.empty((9, 9), dtype=object)
map6 = np.empty((9, 9), dtype=object)

# test run

# find block positions
exploreMapX()  # Explore left side of map and find block 1 and block 2
gotoY()  # Go to (4,4)
exploreMapY()  # Explore right side of map and find block 3 and qr-block 2

print("Initial dry run report:")
print("Block 1: (", block1.x, ",", block1.y, ")")
print("Block 2: (", block2.x, ",", block2.y, ")")
print("QR Block 1: (", qrBLock1.x, ",", qrBLock1.y, ")")
print("Block 3: (", block3.x, ",", block3.y, ")")
print("QR Block 2: (", qrBLock2.x, ",", qrBLock2.y, ")")
print("Going back to start position for mapping phase...")
print("")

gotoX()  # Go to (0,0)

# find map1 - start to block 1
map1 = buildMatrix(block1, 1)
floodFill(block1, map1)

# find map2 - block 1 to block 2
map2 = buildMatrix(block2, 1)
floodFill(block2, map2)

# find map3 - block 2 to qrcode block 1
map3 = buildMatrix(qrBLock1, 1)
floodFill(qrBLock1, map3)

# find map4 - qrcode block 1 to block 3
map4 = buildMatrix(block3, 2)
floodFill(block3, map4)

# find map5 - block 3 to qrcode block 2
map5 = buildMatrix(qrBLock2, 2)
floodFill(qrBLock2, map5)

# find map6 - qrcode block 2 to end
map6 = buildMatrix(endPos, 2)
floodFill(endPos, map6)

bot.pos.x = 0
bot.pos.y = 0
bot.orientation = 1
print("Map 1:")
printMaze(map1, bot)
print("Map 2:")
bot.pos.copyPos(block1)
printMaze(map2, bot)
print("Map 3:")
bot.pos.copyPos(block2)
printMaze(map3, bot)
print("Map 4:")
bot.pos.copyPos(qrBLock1)
printMaze(map4, bot)
print("Map 5:")
bot.pos.copyPos(block3)
printMaze(map5, bot)
print("Map 6:")
bot.pos.copyPos(qrBLock2)
printMaze(map6, bot)

# actual run

a = input("Test run over. Place bot in Start position and press enter:")
bot.pos.x = 0
bot.pos.y = 0
bot.orientation = 1

botMove(block1, map1)
print("Block 1 reached")
botMove(block2, map2)
print("Block 2 reached")
botMove(qrBLock1, map3)
print("QR Block 1 reached")
botMove(block3, map4)
print("BLock 3 reached")
botMove(qrBLock2, map5)
print("QR BLock 2 reached")
map6[8][0].pos.x = 8
botMove(endPos, map6)
print("End reached")

print("Success!")

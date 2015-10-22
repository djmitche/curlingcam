import sys
import time
import numpy
import cv
import cv2


def plotLine(img, rho, theta, color):
    a = numpy.cos(theta)
    b = numpy.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),color,2)

def findVerticalLine(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLines(edges,4,numpy.pi/180,200)
    if lines is None:
        return None

    # select the one with theta closest to zero, as the most vertical line
    line = sorted(lines[0], key=lambda (r,t): abs(t))[0]
    return line

class Processor(object):
    
    def process(self, img):
        pass

    def plot(self, img):
        pass


class LineFinder(Processor):

    def __init__(self, every):
        self.every = every
        self.last = 0
        self.line = None

    def process(self, img):
        if self.every and self.last + self.every > time.time():
            return

        newline = findVerticalLine(img)
        if newline is not None:
            self.line = newline

    def plot(self, img):
        if self.line is None:
            return
        rho, theta = self.line
        plotLine(img, rho, theta, (255, 255, 255))


def video(processors):
    cap = cv2.VideoCapture(0)
    print cap.get(cv.CV_CAP_PROP_FORMAT)
    print cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
    print cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
    print cap.get(cv.CV_CAP_PROP_FPS)

    last_time = time.time()
    while cv2.waitKey(1) == -1:
        ret, frame = cap.read()
        for proc in processors:
            proc.process(frame)
        for proc in processors:
            proc.plot(frame)
        cv2.imshow("frame", frame)
        now = time.time()
        sys.stdout.write("FPS: %.2f" % (1.0 / (now - last_time)) + "\r")
        sys.stdout.flush()
        last_time = now

video([LineFinder(0.5)])

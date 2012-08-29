import time
import marshal
import threading
import sys


# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

def run(dev):
    # sets a variable with the package's internal name
    #package = 'wcho.amazing'
    #runcmd = 'am start -a android.intent.action.MAIN -n wcho.amazing/.Cho_sAmazingApp'
    runcmd = 'am start -a android.intent.action.MAIN -n kr.daum_mobage.am_db.g13000044/com.ngmoco.gamejs.activity.GameJSActivity'
    dev.shell(runcmd)

def wait():
    print 'wait 5 secs'
    time.sleep(5)
    print 'waken'

# Presses the Menu button
#device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)

def up(d):
    d.drag((200,200),(200,237),0.1,1)
    time.sleep(1.1)

def down(d):
    d.drag((200,237),(200,200),0.1,1)
    time.sleep(1)

def gotoStart(d):
    for i in range(3):
        d.drag((50,1000),(50,100),0.1,1)
        time.sleep(1)

def gotoStartElev(d):
    d.drag((500,1000),(500,100),5,1)
    time.sleep(1)

def gotoTop(d):
    for i in range(3):
        d.drag((200,100),(200,1000),0.1,1)
        time.sleep(0.5)
    
# Takes a screenshot
def shot(d):
    result = d.takeSnapshot()
    # Writes the screenshot to a file
    result.writeToFile(str(time.time())+'.png','png')

def clickFloor(d):
    d.touch(500,700,MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickContinue(d):
    d.touch(400,850,MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickYes(d):
    d.touch(500,850,MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickNo(d):
    d.touch(300,850,MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickYesExit(d):
    d.touch(240,750,MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickNoExit(d):
    d.touch(550,750,MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickAlert(d,nth):
    d.touch(95*nth+50, 1150, MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def clickFinishedBusiness(d):
    d.touch(400, 500, MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)

def back(d):
    d.press('KEYCODE_BACK', 'DOWN_AND_UP')
    time.sleep(0.5)

def clickDeliveryMan(d):
    d.touch(70, 860, MonkeyDevice.DOWN_AND_UP)
    time.sleep(0.5)
    
def clickElevUp(d):
    # d.drag((500,1000),(500,100),5,1)
    # time.sleep(1)
    d.touch(280, 1050, MonkeyDevice.DOWN)
    time.sleep(0.05)
    d.touch(280, 1050, MonkeyDevice.UP)
    time.sleep(1.5)

def cropDelivery(img):
    return img.getSubImage((30,1000,100,100))

def cropCloseButton(img):
    return img.getSubImage((690,1170,95,95))

def cropContinueButton(img):
    return img.getSubImage((349,822,95,95))

def cropElevButton(img):
    return img.getSubImage((250,1000,95,95))

def cropExitButton(img):
    return img.getSubImage((90,520,95,95))

def hasCloseButton(d, screen = None):
    if screen == None:
        screen = d.takeSnapshot()
    cb = cropCloseButton(screen)
    cbRaw = getRawImg(cb)
    return equalRawImgs(cbRaw, CLOSEICON)

def hasContinueButton(d, screen = None):
    if screen == None:
        screen = d.takeSnapshot()
    cb = cropContinueButton(screen)
    cbRaw = getRawImg(cb)
    return equalRawImgs(cbRaw, CONTICON)

def hasElevButton(d, screen = None):
    if screen == None:
        screen = d.takeSnapshot()
    btn = cropElevButton(screen)
    btnRaw = getRawImg(btn)
    return equalRawImgs(btnRaw, ELEVICON)

def hasExitButton(d, screen = None):
    if screen == None:
        screen = d.takeSnapshot()
    btn = cropExitButton(screen)
    btnRaw = getRawImg(btn)
    return equalRawImgs(btnRaw, EXITICON)

def getRawImgFromFile(filename):
    f = open(filename, "r")
    return marshal.load(f)

ICON = {
    "deli": getRawImgFromFile("deli.dat"),
    "elev": getRawImgFromFile("elev.dat"),
    "empty": getRawImgFromFile("empty.dat"),
    "finish": getRawImgFromFile("finish.dat"),
    "vip": getRawImgFromFile("vip.dat"),
    }
CLOSEICON = getRawImgFromFile("close.dat")
CONTICON = getRawImgFromFile("cont.dat")
ELEVICON = getRawImgFromFile("elev_btn.dat")
EXITICON = getRawImgFromFile("exit.dat")

def getAlertsType(d, scr = None):
    if scr == None:
        scr = d.takeSnapshot()

    types = []
    alertRawImgs = [getRawImg(img) for img in getAlerts(d, scr)]
    for i in range(len(alertRawImgs)):
        for icon in ICON:
            if equalRawImgs(ICON[icon], alertRawImgs[i]):
                types.append(icon)
                break
    return types


STAT = {'deli':0, 'elev':0, 'finish':0}
def main():
    dev = MonkeyRunner.waitForConnection()
    print 'Connected.'
    dev.drag((200,511), (200,200), 0.1, 1)
    return dev

STOP = 0
class AlertLoopThread(threading.Thread):
    def __init__(self, d):
        threading.Thread.__init__(self)
        self.d = d

    def run(self):
        global STAT
        iter = 0
        while not STOP:
            print "iter", iter
            handleAlert(d)
            time.sleep(3)
            iter = iter + 1
            print STAT
        print "Stop loop!"

def runLoop(d):
    t = AlertLoopThread(d)
    t.start()

def handleAlert(d):
    types = getAlertsType(d)
    print types
    brk = 0

    scr = d.takeSnapshot()
    if hasExitButton(d, scr):
        print "click exit no"
        clickNoExit(d)
        return
    if hasCloseButton(d, scr):
        print "click close"
        back(d)
        return

    for ti in range(len(types)):
        if types[ti] == "finish":
            print "handling finish: ", ti
            clickAlert(d, ti)
            time.sleep(2)
            clickFinishedBusiness(d)
            STAT['finish'] = STAT['finish'] + 1
            return
        elif types[ti] == "deli":
            print "handling delivery: ", ti
            clickAlert(d, ti)
            clickYes(d)
            time.sleep(3)
            findDeli(d)
            STAT['deli'] = STAT['deli'] + 1
            return
    for ti in reversed(range(len(types))):
        if types[ti] == "elev":
            print "handling elevator: ", ti
            clickAlert(d, ti)
            time.sleep(3)
            clickDeliveryMan(d)
            findElev(d)
            STAT['elev'] = STAT['elev'] + 1
            return

def findElev(d):
    elevMode = True
    while elevMode:
        sys.stdout.write('.')
        gotoStartElev(d)
        for ei in range(80):
            screen = d.takeSnapshot()
            if not hasElevButton(d, screen):
                print "Found elevator! at ", ei
                if hasContinueButton(d, screen):
                    back(d)
                if hasCloseButton(d, screen):
                    back(d)
                return
            else:
                clickElevUp(d)
        elevMode = hasElevButton(d)

def getAlerts(d, scr = None):
    if scr == None:
        scr = d.takeSnapshot()
    return listAlerts(scr)

def listAlerts(img):
    x = 0
    y = 1106
    w = 95
    h = 95
    alerts = []
    for i in range(8):
        rect = (x,y,w,h)
        alerts.append(img.getSubImage(rect))
        x = x + w
        y = y
    return alerts

#(349,822,95,95)

def writeSubImgToFileAsRaw(d, rect, filename):
    screen = d.takeSnapshot()
    subimg = screen.getSubImage(rect)
    writeImgToFileAsRaw(filename, subimg)

def writeImgToFileAsRaw(filename, img):
    f = open(filename, "wb")
    marshal.dump(getRawImg(img), f)
    f.close()
    
def saveAlerts(d):
    screen = d.takeSnapshot()
    alerts = listAlerts(screen)
    for i in range(len(alerts)):
        alerts[i].writeToFile("alert"+str(i)+".png", "png")
        writeImgToFileAsRaw("alert"+str(i)+".dat", alerts[i])

def getRawImg(img):
    return [img.getRawPixelInt(x,y) for x in range(95) for y in range(95)]

def equalRawImgs(i1, i2):
    return compareRawImgs(i1, i2) < 0.3

def compareRawImgs(i1, i2):
    size = len(i1) * 1.0
    diff = reduce(lambda acc,d: acc if d == 0 else acc+1, [((0xffffff & i1[i]) - (0xffffff & i2[i])) for i in range(size)], 0) / size
    #print diff
    return diff

def findDeli(d):
    gotoStart(d)
    time.sleep(1)
    for i in range(80):
        clickFloor(d)
        sys.stdout.write('.')
        if i % 10 == 9 and not hasContinueButton(d):
            back(d)
            print "Found! at", i
            break
        else:
            back(d)
        up(d)


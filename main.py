import cv2 as cv
import time
import HandDetectionModule
import math
import  pyautogui
HandDetector = HandDetectionModule.HandDetector(mode=False,MaxHands=2,DetectionConfidance=0.6,TrackConfidence=0.6)
# Camera Setting
cap = cv.VideoCapture(0)
CamWidth ,CamHeight =900,900
cap.set(3,CamWidth)
cap.set(4,CamHeight)

# fps Variables
CurrentTime =0
PreviousTime = 0
fps = 0

#global variables
CurrentMiddleFingerPoint = [0, 0]  #
CurrentPalmPoint  = [0, 0]
PreviousPalmPoint = [0,0]


# Threshold Distances
PalmDistancemin = 100 # Distance Between Middle and Palm point
MovementThreshold = 7 # Recognise movement Threshold
def FindMovemetnt(CurrentPoint,PreviousPoint):
    dist = GetDistance( CurrentPalmPoint, CurrentMiddleFingerPoint )
    if dist > PalmDistancemin :
        differ_x = int(PreviousPoint[0]-CurrentPoint[0])
        differ_y =int(PreviousPoint[1] - CurrentPoint[1])
        radians = math.atan2( differ_y, differ_x )
        angle = (math.degrees( radians ))
        if math.fabs(differ_x)>MovementThreshold :
            # Left 
            if angle > -35 and angle < 30:
                # print("Left")
                pyautogui.press( pyautogui.LEFT )

                #Right
            elif angle >140 or angle < -140:
                pyautogui.press(pyautogui.RIGHT)
                # print("Right")
        if math.fabs(differ_y) > MovementThreshold:
            # Up
            if angle > 30 and angle < 140:
                # print("up")
                pyautogui.press('up')
                # Down    
            elif angle >-140  and angle <-35:
                # print("down")
                pyautogui.press('down')

def pause(img) :

    FoundHands = HandDetector.GetHands()
    if (FoundHands):
        ImgShape = img.shape
        if len( FoundHands ) == 2:

            MiddleFingerPos = []
            PalmPos = []
            for Hand in FoundHands:
                for id, landmark in enumerate( Hand.landmark ):

                    if id == 0:
                        height, width, channel = ImgShape
                        posx, posy = int( landmark.x * width ), int( landmark.y * height )
                        PalmPos.append( [posx, posy] )
                    if id == 12:
                        height, width, channel = ImgShape
                        posx, posy = int( landmark.x * width ), int( landmark.y * height )
                        MiddleFingerPos.append( [posx, posy] )
            if MiddleFingerPos and PalmPos:

                if GetDistance( MiddleFingerPos[0], PalmPos[0] ) > PalmDistancemin:
                    if GetDistance( MiddleFingerPos[1], PalmPos[1] ):
                        pyautogui.press( "space" )

def GetDistance (Point1,Point2):
   return math.dist(Point1,Point2)


def main():
    global PreviousTime
    while cap.isOpened():
        success, image = cap.read()
        CurrentTime = time.time()
        image=  cv.flip( image, 1 )
        if(CurrentTime-PreviousTime)!=0:
            fps = 1 / (CurrentTime - PreviousTime)
        PreviousTime = CurrentTime
        cv.putText( image, str( "FPS: " + str( int( fps ) ) ), (10, 70), cv.FONT_HERSHEY_PLAIN, 2, (225, 50, 225), 2 )
        HandDetector.FindHands( image, True )

        HandLandMarks_List = HandDetector.FindPositions( image, 0, False )
        if len( HandLandMarks_List ) != 0 and HandDetector.GetNoOfHands() <2:
            CurrentMiddleFingerPoint[0] = HandLandMarks_List[12][1]
            CurrentMiddleFingerPoint[1] = HandLandMarks_List[12][2]
            CurrentPalmPoint[0] = HandLandMarks_List[0][1]
            CurrentPalmPoint[1] = HandLandMarks_List[0][2]
            FindMovemetnt( CurrentPalmPoint, PreviousPalmPoint )
            PreviousPalmPoint[0] = CurrentPalmPoint[0]
            PreviousPalmPoint[1] = CurrentPalmPoint[1]
            cv.circle( image, (CurrentPalmPoint[0], CurrentPalmPoint[1]), 10, (0, 225, 0), None, cv.FILLED )

        if HandDetector.GetNoOfHands() >1:
            pause(img=image)
        cv.imshow( "Video Viewer", image )
        if cv.waitKey( 5 ) & 0xFF == 27:
            break

if __name__ == '__main__':
    main()
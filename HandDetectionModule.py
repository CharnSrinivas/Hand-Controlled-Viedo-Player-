import cv2 as cv
import mediapipe as mp
import time
NoOfHands = 0
FoundHands = []
class HandDetector():

    def __init__(self,mode=False,MaxHands=2,DetectionConfidance=0.5,TrackConfidence=0.5):

        self.mode= mode
        self.MaxHands = MaxHands
        self.DetectionConfidence =DetectionConfidance
        self.TrackConfidence=TrackConfidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.MaxHands,self.DetectionConfidence,self.TrackConfidence)
        self.MpDraw = mp.solutions.drawing_utils

    def FindHands(self,img,draw =True):
        imgRGB = cv.cvtColor( img, cv.COLOR_BGR2RGB )
        self.results = self.hands.process( imgRGB )

        # print(results.multi_hand_landmarks)
        # cv.putText( img, str( int( fps ) ), (10, 70), cv.FONT_ITALIC, 3, (225, 50, 225), 2 )
        if self.results.multi_hand_landmarks:

            for hand_land_mark in self.results.multi_hand_landmarks:
                if draw:
                    self.MpDraw.draw_landmarks( img,  hand_land_mark, self.mpHands.HAND_CONNECTIONS )

        return img

    def FindPositions(self,img,HandNo=0,draw=True):
        landmark_list =[]
        global FoundHands
        FoundHands = self.results.multi_hand_landmarks
        if FoundHands:

            #selecting any one hand
            OneHand = FoundHands[HandNo]
            global NoOfHands
            NoOfHands = len(FoundHands)

            for id, landmark in enumerate( OneHand.landmark ):
                height, width, channel = img.shape

                posx, posy = int( landmark.x * width ), int( landmark.y * height )
                # adding  positions of all dots

                landmark_list.append( [id, posx, posy] )
                if draw:
                    cv.circle( img, (posx, posy), 10, (22, 0, 0,), cv.FILLED )


        return landmark_list
    def GetNoOfHands(self):
        return NoOfHands
    def GetHands(self):
        return FoundHands

def main():
    cap = cv.VideoCapture(0)

    CurrentTime =0
    PreviousTime = 0
    fps =0
    detector = HandDetector()
    while True:

        success,img = cap.read()
        img =   detector.FindHands(img,True)
        landmark_list =  detector.FindPosition(img,0,True)
        if len(landmark_list) != 0:
            print(landmark_list[8])



        cv.imshow("image",img)

        cv.waitKey(1)

if __name__ == '__main__':
    main()



import cv2
import mediapipe as mp
import time
import math
 


"""
__summary_:
Stand-Alone Class for hand detection.
Finds Hands using the mediapipe library. Exports the landmarks
in pixel format. Adds extra functionalities like finding how
many fingers are up or the distance between two fingers. Also
provides bounding box info of the hand found.
"""


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20] ### tip of all the five fingers in media-pipe specification


    def get_thumb_landmark(self):
        """_summary_: getter for thumb landmark - easy access
        Returns:
            list (int): coordinates of the thumb landmark
        """
        if self.landmark_list != []:
            return self.landmark_list[self.tipIds[0]][1:]

    def get_index_finger_landmark(self):
        """_summary_: getter for index finger landmark - easy access
        Returns:
            list (int): coordinates of the index finger landmark
        """
        if self.landmark_list != []:
            return self.landmark_list[self.tipIds[1]][1:]  

    def get_middle_finger_landmark(self):
        """_summary_: getter for middle finger landmark - easy access
        Returns:
            list (int): coordinates of the middle finger landmark
        """
        if self.landmark_list != []:
            return self.landmark_list[self.tipIds[2]][1:]
    
    def get_ring_finger_landmark(self):
        """_summary_: getter for ring landmark - easy access
        Returns:
            list (int): coordinates of the ring landmark
        """
        if self.landmark_list != []:
            return self.landmark_list[self.tipIds[3]][1:]

    def get_little_finger_landmark(self):
        """_summary_: getter for little finger landmark - easy access
        Returns:
            list (int): coordinates of the little landmark
        """
        if self.landmark_list != []:
            return self.landmark_list[self.tipIds[5]][1:]


    
    def find_hands(self, img, draw=True):
        """
        _summary_: finds/detects hands from the image provided, 
                   displays the image with all the landmarks on to the screen

        Parameters
        ----------
        img: <class 'numpy.ndarray'>
            __description_, img as clear by it's name is an acutal image represented as a 2D numpy array 
        draw: Boolean, optional
            _description_, by default True, draws the hand detected on the window/screen


        Returns
        -------
        _type_, img: <class 'numpy.ndarray'>
            _description_ img with on
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    
 
    def find_landmarks_pos(self, img, handNo=0, draw=True):
        """
        _summary_: finds/detects all the x and y coordinates of all the landmarks in given hand
                   draws a rectangle around the detected hand by default - could be turned off 


        Args:
            img <class 'numpy.ndarray'>: img as clear by its name is an acutal image represented as a 2D numpy array 
            handNo (int, optional): number of hand. Defaults to 0.
            draw (bool, optional): boolean value to draw a rectangle around the hand. Defaults to True.

        Returns:
            list: contains integer values for LandMark_ID, X-Coordinate, and Y-Coordinate of the specified LandMArk_ID
            tuple: the top-left x and y coordinates, and bottom-right x and y coordinates
        """

        x_coordinates = []
        y_coordinates = []
        bounding_box = [] #rectangle to encapsulate the hand-landmarks
        self.landmark_list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for landmark_id, landmark in enumerate(myHand.landmark):
                h, w, _ = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                x_coordinates.append(cx)
                y_coordinates.append(cy)
                self.landmark_list.append([landmark_id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
 
            xmin, xmax = min(x_coordinates), max(x_coordinates)
            ymin, ymax = min(y_coordinates), max(y_coordinates)
            bounding_box = xmin, ymin, xmax, ymax
 
            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)
        return self.landmark_list, bounding_box


    def list_open_fingers(self):
        """
        _summary_: checks wheter fingers are opened or closed
                   checks every single tip of every single finger and based off of its relative position
                   to the second-last landmark of the fingers decide whether its open or closed
        Returns: 
            list: integers list containing either 0 or 1
        """
        fingers = []
        # Thumb Detection
        if self.landmark_list[self.tipIds[0]][1] > self.landmark_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # Other Fingers Detection
        for tip_index in range(1, 5):
            if self.landmark_list[self.tipIds[tip_index]][2] < self.landmark_list[self.tipIds[tip_index] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    

    def is_hand_open(self):
        print(self.list_open_fingers())
        if all(item == 0 for item in  self.list_open_fingers()[1:]): 
            return False 
        else: 
            return True


    def is_thumb_open(self):
        """_summary_: checks whether the thumb is open or closed

        Returns:
            Bool: if the thumb is open, returns True - False otherwise
        """
        return True if  self.list_open_fingers()[0] == 1 else False 


    def is_index_finger_open(self):
        """_summary_: checks whether the index finger is open or closed

        Returns:
            Bool: if the index finger is open, returns True - False otherwise
        """
        return True if self.list_open_fingers()[1] == 1 else False
    
    def is_middle_finger_open(self):
        """_summary_: checks whether the middle finger is open or closed

        Returns:
            Bool: if the middle finger is open, returns True - False otherwise
        """
        return True if self.list_open_fingers()[2] == 1 else False

    
    def is_ring_finger_open(self):
        """_summary_: checks whether the ring finger is open or closed

        Returns:
            Bool: if the ring finger is open, returns True - False otherwise
        """
        return True if self.list_open_fingers()[3] == 1 else False

    def is_little_finger_open(self):
        """_summary_: checks whether the little finger is open or closed

        Returns:
            Bool: if the little finger is open, returns True - False otherwise
        """
        return True if self.list_open_fingers()[4] == 1 else False


    def find_distance_between_landmarks(self, landmark1, landmark2, img, draw=True,radius=15, thickness=3):
        """
        _summary_: finds distance between two landmarks of the same hand
                   draws a line between the two landmarks if draw is True 
                   draws a circle in the center of landmarks if draw is True

        Args:
            landmark1 (int): first landmark of the hand 
            landmark2 (int): second landmark of the hand
            img (<class 'numpy.ndarray'>): img as clear by its name is an acutal image represented as a 2D numpy array 
            draw (bool, optional): boolean value whether to draw a line between the landmarks. Defaults to True.
            radius (int, optional): randius of the circle to be drawn fro the landmarks. Defaults to 15.
            thickness (int, optional): thickness of the line. Defaults to 3.

        Returns:
            length (int): length between the landmarks 
            img (<class 'numpy.ndarray'>): img as clear by its name is an acutal image represented as a 2D numpy array 
            list (int): information about x and y coordinates of each landmark and their center
        """

        x1, y1 = self.landmark_list[landmark1][1:]
        x2, y2 = self.landmark_list[landmark2][1:]
        mid_point_x, mind_point_y = (x1 + x2) // 2, (y1 + y2) // 2
        coordinate_info = [x1, y1, x2, y2, mid_point_x, mind_point_y]

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), thickness)
            cv2.circle(img, (x1, y1), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (mid_point_x, mind_point_y), radius, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, coordinate_info
 
 
def main():
    """
    _summary_: to test the functions of the class
    """

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector(1)
    while True:
        success, img = cap.read()
        #print(type(img))
        img = detector.find_hands(img= img)
        lmList, bbox = detector.find_landmarks_pos(img)
        if len(lmList) != 0:
            if detector.is_hand_open():
                print("Hand Open")
            else: 
                print("Hand Closed")
            # #print(lmList[4])
            # if detector.is_index_finger_open(): 
            #     print("Index - Open")
            # else:
            #     print("Index - Closed")
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)
 
 
if __name__ == "__main__":
    main()
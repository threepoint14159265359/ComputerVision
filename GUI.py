import cv2


class Button: 
    def __init__(self, img,start_x, start_y, end_x, end_y, color, text) -> None:
        self.img = img
        self.start_x = start_x 
        self.start_y = start_y 
        self.end_x = end_x 
        self.end_y = end_y 
        self.color = color 
        self.text = text
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.9
        self.white_color = (255,255,255)
        self.hover = True
        self.__create()
        

    def __create(self):
        if self.hover:
            cv2.rectangle(self.img, (self.start_x - 5, self.start_y - 5), (self.end_x + 5, self.end_y + 5), self.color[1] - 1 , cv2.FILLED)
        else: 
            cv2.rectangle(self.img, (self.start_x, self.start_y), (self.end_x, self.end_y), self.color, cv2.FILLED)
        cv2.putText(self.img,self.text, ( int((self.start_x+self.end_x)/2) - 35,  int((self.start_y+self.end_y)/2) + 10)  , self.font, self.font_scale , self.white_color, 2)

    def hover(self, event, x, y, flags, params):
        if x > self.start_x and x < self.start_y and y > self.start_y and y < self.end_y: 
            self.hover = True
        else: 
            self.hover = False 
    
    def is_clicked(self):
        pass

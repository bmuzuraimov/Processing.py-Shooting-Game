import random as rd
class Robot(object):
    def __init__(self, x, y, x1, y1, scle, max_scle, lane):
        self.hp = 100
        self.lane = lane
        self.x_pure = None
        self.y_pure = None
        self.x_pos = None
        self.y_pos = None
        self.scle = scle
        self.max_scle = max_scle
        self.set_pos(x, y)
        self.end_x_pos = 0
        self.end_y_pos = 0
        self.dy = (y1-y)/1300
        self.dx = (x1-x)/1000
        self.dscle = (max_scle-scle)/1300
        self.isMove = False
        self.edges = [self.y_pos-180, self.x_pos+105, self.y_pos+180, self.x_pos-105]
        self.message = ""
        self.isMoving = False
        self.isShoot = False
        self.isSpin = False
        self.isHacked = False
        self.isFalling = False
        self.falling_speed = 1
        
    def __drawAntenna(self, x, y):
        # y_axis is range between 0 and 90
        o_pos = [x, y-172, 15, x, y-165, x-2, y-130, x+2, y-130]
        r = 0
        g = 255
        b = 0
        if(self.isShoot):
            fill(255, 10, 10)
        else:
            fill(10, 255, 10)
        circle(o_pos[0], o_pos[1], o_pos[2])
        fill(210)
        triangle(o_pos[3], o_pos[4], o_pos[5], o_pos[6], o_pos[7], o_pos[8])
        
    def __drawFace(self, x, y):
        o_pos = [x, y-100, 80, 60, 5, x-20, y-115, 23, 12, x+20, y-115, 23, 12]
        # face
        fill(210)
        rect(o_pos[0], o_pos[1], o_pos[2], o_pos[3], o_pos[4])
        fill(20)
        rect(x, y-100, 65, 45, 5)
        # eyes
        fill(0, 79, 195)
        if mouseX > (x+30):
            r_range = map(mouseX, width/2, width, 0, 6)
            left_x = x-20+r_range;
            right_x = x+20+r_range
        elif mouseX < (x-30):
            l_range = map(mouseX, 0, width/2, -6, 0)
            left_x = x-20+l_range;
            right_x = x+20+l_range
        else:
            left_x = x-20;
            right_x = x+20 
        noStroke()
        rect(left_x, y-105, 10, 5)
        rect(right_x, y-105, 10, 5)
        stroke(1)
        
    def __drawNeck(self, x, y):
        # neck 
        fill(210)
        rect(x, y-60, 30, 20)
        for i in range(y-70, y-50, 3):
            line(x-15, i, x+15, i)
        rect(x, y-47, 40, 5)
    
    def __drawBody(self, x, y):
        # body
        fill(210)
        rect(x, y-40, 100, 10)
        rect(x, y+25, 80, 120)
        # screen 
        fill(255)
        rect(x, y+15, 70, 70)
        self.__displayMessage(x, y, self.message)
        bar_color = self.__red2green(self.hp)
        fill(bar_color[0], bar_color[1], bar_color[2])
        if(self.hp >= 0):
            rect(x-35+(0.7 * self.hp / 2), y+53, (0.7 * self.hp), 6)
        
    def __displayMessage(self, x, y, message=""):
        if (not self.isHacked):
            textSize(14)
            fill(0, 0, 255)
            text(message, x, y+14)
            noFill()
        else:
            textSize(11)
            for i in range(y-10, y+60, 12):
                message = list("10101010")
                rd.shuffle(message)
                message = ''.join(message)
                if i == y+14 and frameCount%4==0:
                    fill(255, 0, 0)
                    text("Hacked!", x, i)
                    continue
                fill(0, 255, 0)
                text(message, x, i)
        
    def __drawButton(self, x, y, col):
        colors = {"red":[255,0,0], "green":[0,255,0], "blue":[0, 0, 255]}
        fill(255)
        circle(x, (y+3)+70, 15)
        fill(colors[col][0], colors[col][1], colors[col][2])
        circle(x, y+70, 15)
        noFill()
    
    def __drawHands(self, x, y):
        left_center = [x-85, y+40]
        right_center = [x+85, y+40]
        fill(210)
        quad(x-40, y-20, x-40, y, x-70, y+30, x-75, y+25)
        quad(x+40, y-20, x+40, y, x+70, y+30, x+75, y+25)
        fill(100, 170, 227)
        circle(left_center[0], left_center[1], 40)
        circle(right_center[0], right_center[1], 40)
        fill(0)
        circle(left_center[0], left_center[1], 10)
        circle(right_center[0], right_center[1], 10)
        fill(255)
        start_deg = 0
        if(self.isShoot==True):
            if frameCount%2==0:
                fill(242, 255, 0)
                start_deg = 30
            for deg in range(start_deg, 360, 60):
                left_x = 15 * cos(radians(deg))
                left_y = 15 * sin(radians(deg))
                circle(left_center[0]+left_x, left_center[1]+left_y, 5)
                right_x = 15 * cos(radians(360-deg))
                right_y = 15 * sin(radians(360-deg))
                circle(right_center[0]+right_x, right_center[1]+right_y, 5)
        
    def __drawWheel(self, x, y):
        fill(220)
        quad(x-40, y+85, x-30, y+85, x-15, y+135, x-15, y+145)
        quad(x+30, y+85, x+40, y+85, x+15, y+145, x+15, y+135)
        rect(x-12, y+140, 5, 20, 2)
        rect(x+13, y+140, 5, 20, 2)
        fill(150)
        rect(x, y+140, 20, 80, 3)
        y_line = 0;
        if(self.isSpin):
            y_line =+ frameCount%6
            for i in range((y+105+y_line), (y+180+y_line), 5):
                line(x-10, i, x+10, i) 
        else:
            for i in range(y+105, y+180, 5):
                line(x-10, i, x+10, i)
        
    def __drawBolts(self, x, y):
        boltXY = [[-35, -75], [35, -125], [-35, -125], [35, -75], [-35, -30], [35, -30],
            [-35, 80], [35, 80]]
        fill(180, 180, 180)
        for boltX, boltY in boltXY:
            circle(x+boltX, y+boltY, 3)
        
    def __red2green(self, percentage = 100):
        rgb_color = []
        red_tint = 0
        green_tint = 0
        if(percentage < 50):
            green_tint = (((percentage - 0) * (255 - 0)) / (50 - 0)) + 0
            green_tint = round(green_tint)
            rgb_color = [255, green_tint, 0]
        else:
            red_tint = (((percentage - 50) * (0 - 255)) / (100 - 50)) + 255
            red_tint = round(red_tint)
            rgb_color = [red_tint, 255, 0]
            
        return rgb_color

    def display(self, bullets):
        if(self.hp >= 0):
            pushMatrix()
            scale(self.scle)
            if(self.scle >= 1):
                x_trans = -1*((width/2)*(self.scle-1))/self.scle
                y_trans = -1*((height/2)*(self.scle-1))/self.scle
            else:
                x_trans = (width/2)*(1-self.scle)/self.scle
                y_trans = (height/2)*(1-self.scle)/self.scle
            translate(x_trans, y_trans)
            mouse_x = (mouseX/self.scle)-x_trans
            mouse_y = (mouseY/self.scle)-y_trans
            if ((mousePressed == True) and (self.x_pos-32 < mouse_x) 
                    and (mouse_x < self.x_pos+32) and (self.y_pos-122 < mouse_y) 
                    and (mouse_y < self.y_pos-78) and bullets > 0):
                self.hp -= 10
                self.isShoot = True
                self.isHacked = True
            self.__drawAntenna(self.x_pos, self.y_pos)
            self.__drawFace(self.x_pos, self.y_pos)    
            self.__drawNeck(self.x_pos, self.y_pos)
            self.__drawBody(self.x_pos, self.y_pos)
            self.__drawButton(self.x_pos-20, self.y_pos, "red")
            self.__drawButton(self.x_pos, self.y_pos, "green")
            self.__drawButton(self.x_pos+20, self.y_pos, "blue")
            self.__drawHands(self.x_pos, self.y_pos)
            self.__drawWheel(self.x_pos, self.y_pos)
            self.__drawBolts(self.x_pos, self.y_pos)
            popMatrix()
            if(frameCount%2 == 0 and self.isMoving and self.scle < self.max_scle):
                self.x_pure -= self.dx
                self.y_pure += self.dy
                self.scle += self.dscle
                self.set_pos(self.x_pure, self.y_pure)
        
    def set_hp(self, hp):
        self.hp = self.hp + hp
        
    def set_pos(self, x, y):
        if(x != self.x_pure):
            self.x_pure = x
            self.x_pos = (width/2) - (((width/2)-x)/self.scle)
            self.x_pos = int(round(self.x_pos))
        if(y != self.x_pure):
            self.y_pure = y
            self.y_pos = (height/2) - (((height/2)-y)/self.scle)
            self.y_pos = int(round(self.y_pos))
        

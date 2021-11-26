import random as rd
class Game(object):
    def __init__(self):
        
        # Graphic settings
        rectMode(CENTER)
        textAlign(CENTER)
        imageMode(CENTER)
        noCursor()
        self.isMouseReleased = False
        
        # Load background images
        self.welcome_bg = loadImage('welcome_bg.jpg')
        self.game_board_bg = loadImage('game_board.jpg')
        self.records_bg = loadImage('records.jpg')
        self.end_game_bg = loadImage('end_game.jpg')
        
        # load game images
        self.gun = loadImage("gun.png")
        self.gun_fire = loadImage('gun_fire.png')
        self.hp_icon = loadImage('user_hp.png')
        self.back_btn = loadImage('back_btn.png')
        self.arrows = [loadImage('arrow_'+str(i)+'.png') for i in range(4)]
        
        self.minute = 0
        self.second = 0
        self.millisecond = 0
        self.currentTime = 0
        self.startTime = 0
        # Calibration variables
        self.bar_heights_top = []
        self.bar_heights_bottom = []
        self.bar_additives = []
        self.bar_color = 255
        self.speed = -6
        self.process_1 = False
        self.openDoor = False
        self.cal_points =  [False for i in range(4)]
        self.isSnipe = False
        self.isCalibrated = False
        
        # Game page logic
        self.player_num = ''
        self.myscore = 0
        self.player_hp = 1200
        self.game_robots = []
        self.isGeneratedRobots = False
        self.isCalibrationPage = True
        self.isStartingPage = False
        self.isGamePage = False
        self.isRecordsPage = False
        self.isEndGame = False
        self.cal_start_time = 0
        self.__create_doors()
        # snipe variables
        self.laser_init_deg = 0
        self.inner_rad = 15
        self.outer_rad = 20
        # lane load to distribute robots evenly
        self.lane_load = [1]*9
        
        # menu button variables
        self.we_btns = []
        self.we_btns_h = []
        y = (height/2)-128
        for btn in range(3):
            self.we_btns.append([0]*9)
            self.we_btns[btn][0] = loadImage('we_bt_'+str(btn)+'.png')
            self.we_btns[btn][1] = width/2
            self.we_btns[btn][2] = y
            self.we_btns[btn][3] = 256
            self.we_btns[btn][4] = 64
            self.we_btns_h.append([0]*9)
            self.we_btns[btn][5] = self.we_btns[btn][2] - (self.we_btns[btn][4]/2)
            self.we_btns[btn][6] = self.we_btns[btn][1] + (self.we_btns[btn][3]/2)
            self.we_btns[btn][7] = self.we_btns[btn][2] + (self.we_btns[btn][4]/2)
            self.we_btns[btn][8] = self.we_btns[btn][1] - (self.we_btns[btn][3]/2)
            self.we_btns_h[btn][0] = loadImage('we_bt_h_'+str(btn)+'.png')
            self.we_btns_h[btn][1] = width/2
            self.we_btns_h[btn][2] = y
            self.we_btns_h[btn][3] = 256
            self.we_btns_h[btn][4] = 64
            self.we_btns_h[btn][5] = self.we_btns_h[btn][2] - (self.we_btns_h[btn][4]/2)
            self.we_btns_h[btn][6] = self.we_btns_h[btn][1] + (self.we_btns_h[btn][3]/2)
            self.we_btns_h[btn][7] = self.we_btns_h[btn][2] + (self.we_btns_h[btn][4]/2)
            self.we_btns_h[btn][8] = self.we_btns_h[btn][1] - (self.we_btns_h[btn][3]/2)
            y += 128
        # End game variables
        self.isRecordsFetched = False
        self.message = None
        self.bullets = 30
        self.isReloading = False
        self.reload_time = 0
        self.gun_angle = 0
        
    def __create_doors(self):
        for bar in range(width/40, width, width/20):
            additives = rd.randint(0, 60)
            self.bar_additives.append(additives)
            bar_height_top = (height/2) - additives + 1
            bar_height_bottom = (height/2) + additives
            self.bar_heights_top.append(bar_height_top) 
            self.bar_heights_bottom.append(bar_height_bottom)

    def set_calibration(self):
        noStroke()
        fill(230, 0, 0)
        if(self.cal_points[0] == False):
            circle(20, 20, 10)
            image(self.arrows[0], 70, 70, 60, 60)
        elif(self.cal_points[0] and self.cal_points[1] == False):
            circle(width-20, 20, 10)
            image(self.arrows[1], width-70, 70, 60, 60)
        elif(self.cal_points[1] and self.cal_points[2] == False):
            circle(20, height-20, 10)
            image(self.arrows[2], 70, height-70, 60, 60)
        elif(self.cal_points[2] and self.cal_points[3] == False):
            circle(width-20, height-20, 10)
            image(self.arrows[3], width-70, height-70, 60, 60)
        textSize(30)
        if self.isCalibrated and (millis()-self.cal_start_time) < 3000:
            self.isSnipe = True
            text('Calibration finished!', width/2, height/2)
        elif(not self.isCalibrated):
            fill(0, 0, 200)
            text('Please calibrate your gun!', width/2, (height/2)-150)
        else:
            self.openDoor = True
        stroke(1)
        
    def starting_page_animation(self): 
        textSize(48)
        counter = 0
        noStroke()
        # process one
        for x in range(width/40, width, width/20):
            bar_height_top = self.bar_heights_top[counter]+self.bar_additives[counter]
            bar_heigth_bottom = self.bar_heights_bottom[counter]-self.bar_additives[counter]
            g = self.bar_color * 2 / 3
            fill(self.bar_color, 255, 255)
            rect(x, bar_height_top/2, (width/20)+1, bar_height_top)
            rect(x, height-(bar_heigth_bottom/2), (width/20)+1, bar_heigth_bottom)
            counter += 1
        if self.openDoor and ((max(self.bar_heights_top) > 0) or (max(self.bar_heights_bottom) > 0)):
            for i in range(len(self.bar_additives)):
                if (self.bar_additives[i] - 3) > 0:
                    self.bar_additives[i] -= (height/150) 
                else:
                    self.bar_additives[i] = 0
            self.process_1 = True
            self.bar_color -= 1.5
            
        if(self.openDoor and self.process_1):
            speed = 0.1*(self.speed**2)
            if(max(self.bar_heights_top)>0):
                self.bar_heights_top = [max(0, x-speed) for x in self.bar_heights_top if (x-speed) > 0 else 0]
            if(max(self.bar_heights_bottom)>0):
                self.bar_heights_bottom = [max(0, i-speed) for i in self.bar_heights_bottom if (i-speed) > 0 else 0]
            if(self.speed < 10):
                self.speed += 0.75
            if(max(self.bar_heights_bottom)==0):
                self.isCalibrationPage = False
        stroke(1)
            
    def starting_page(self):
        image(self.welcome_bg, width/2, height/2, width, height)
        for btn in range(3):
            if ((self.we_btns[btn][8] < mouseX) and (mouseX < self.we_btns[btn][6]) and (self.we_btns[btn][5] < mouseY) and (mouseY < self.we_btns[btn][7])):
                image(self.we_btns_h[btn][0], self.we_btns_h[btn][1], self.we_btns_h[btn][2], self.we_btns_h[btn][3], self.we_btns_h[btn][4])
                if(mousePressed):
                    if(btn == 0):
                        self.isGamePage = True
                        self.isStartingPage = False
                    elif(btn == 1):
                        self.isRecordsPage = True
                        self.isStartingPage = False
                    else:
                        exit()
            else:
                image(self.we_btns[btn][0], self.we_btns[btn][1], self.we_btns[btn][2], self.we_btns[btn][3], self.we_btns[btn][4])
                
    def game_page(self):
        if(not self.isRecordsFetched):
            self.isRecordsFetched = True
            f = open('data/records.txt', 'r')
            records = f.readlines()
            f.close()
            last_player = 0
            for player in records:
                player = player.strip()
                if(player == ''):
                    continue
                player = player.split()[1]
                if (int(player) > last_player):
                    last_player = int(player)
            self.player_num = str(last_player+1)
        if(self.player_hp <= 0):
            self.isGamePage = False
            self.isEndGame = True
            self.isRecordsFetched = False
            self.bullets = 30
        if(self.bullets == 0 and not self.isReloading):
            self.reload_time = millis()
            self.isReloading = True
        if(millis() - self.reload_time > 2000 and self.bullets == 0):
            self.bullets = 30
            self.isReloading = False
        image(self.game_board_bg, width/2, height/2, width, height)
        if(self.startTime == 0):
            self.startTime = millis()
        self.currentTime = millis() - self.startTime
        self.minute = self.currentTime / 1000 / 60
        self.second = (self.currentTime / 1000) % 60
        if(mousePressed and self.bullets > 0):
            image(self.gun_fire, width/1.4, height-135)
            pushMatrix()
            rotate(0.1)
            translate(85, -85)
            image(self.gun, width*3/4, height-85, 170, 170)
            popMatrix()
            self.bullets -= 1
        else:
            image(self.gun, width*3/4, height-85, 170, 170)
        textAlign(LEFT)
        textSize(18)
        fill(255,218,102)
        text('Score: '+str(self.myscore), 10, 20)
        text('Time: {}:{}'.format(self.minute, self.second), 10, 40)
        textAlign(CENTER)
        hp_x = [40, 80, 120, 160, 200]
        for i in range(((self.player_hp-1)//300)+1):
            image(self.hp_icon, hp_x[i], height-40, 30, 30)
        textSize(22)
        text('User '+self.player_num, width/2, 25)
        reload_time = min(millis()- self.reload_time, 2000)
        reload_length = reload_time*0.12
        reload_time = str(reload_time/1000)+' sec'
        text(reload_time, width/2-160, height-30)
        rect(width/2, height-40, reload_length, 20)

    def records_page(self):
        image(self.records_bg, width/2, height/2, width, height)
        image(self.back_btn, 50, 50)
        if(mousePressed and self.overCircle(50, 50, 70)):
            self.isRecordsPage = False
            self.isStartingPage = True
            self.isRecordsFetched = False
        if(not self.isRecordsFetched):
            f = open('data/records.txt', 'r')
            records = f.readlines()
            f.close()
        y = (height/2)-100
        textSize(48)
        for record in records:
            text(record, width/2, y)
            y += 48
            
    def end_game_page(self):
        image(self.end_game_bg, width/2, height/2, width, height)
        fill(255,218,102)
        textSize(60)
        text('Game Over!', width/2, 200)
        textSize(38)
        if(not self.isRecordsFetched):
            f = open('data/records.txt', 'r')
            records = f.readlines()
            f.close()
            best_player = [None]*3
            for record in records:
                record = record.strip()
                rec = record.split()
                if(record == ''):
                    continue
                elif (int(rec[3]) > best_player[0]):
                    best_player[0] = int(rec[3])
                    best_player[1] = rec[0]
                    best_player[2] = rec[1]
                if(self.myscore > int(best_player[0])):
                    self.message = 'Congrats! You beat the record with {} {}'.format(self.myscore, 'points')
                else:
                    self.message = 'The best is: {} by {} {}\nYour Score: {}'.format(best_player[0], best_player[1], best_player[2], self.myscore)
            self.isRecordsFetched = True
            new_record = 'User {} - {} points\n'.format(self.player_num, self.myscore)
            records.append(new_record)
            records = sorted(records, key = lambda x : int(x.split()[3]))
            if(len(records)>5):
                records = records[-5:]
            new_records = ''
            for record in records:
                new_records += record
            f = open('data/records.txt', 'w')
            f.write(new_records)
            f.close()
        text(self.message, width/2, 280)
        image(self.we_btns_h[0][0], self.we_btns_h[0][1], 410, self.we_btns_h[0][3], self.we_btns_h[0][4])
        image(self.we_btns_h[2][0], self.we_btns_h[2][1], 490, self.we_btns_h[2][3], self.we_btns_h[2][4])
        if (mousePressed and (self.we_btns[0][8] < mouseX) and (mouseX < self.we_btns[0][6]) and (378 < mouseY) and (mouseY < 442)):
            self.isRecordsFetched = False
            self.isGamePage = True
            self.isEndGame = False
            self.player_hp = 1200
            self.myscore = 0
            self.isGeneratedRobots = False
            self.game_robots = []
            self.startTime = millis()
        if (mousePressed and (self.we_btns[2][8] < mouseX) and (mouseX < self.we_btns[2][6]) and (458 < mouseY) and (mouseY < 522)):
            exit()
                
    def draw_snipe(self, x, y):
        fill(255, 0, 0)
        strokeWeight(3)
        stroke(251,210,85)
        strokeCap(ROUND)
        line(x, y, x-4, y+8)
        line(x, y, x+4, y+8)
        for deg in range(self.laser_init_deg, 360+self.laser_init_deg, 18):
            rad = radians(deg)
            inner_x = self.inner_rad * cos(rad) 
            inner_y = self.inner_rad * sin(rad)
            outer_x = self.outer_rad * cos(rad) 
            outer_y = self.outer_rad * sin(rad)
            line(x+inner_x, y+inner_y, x+outer_x, y+outer_y)
        if(self.inner_rad > 15):
            self.inner_rad -= 0.5
            self.outer_rad -= 0.5
        stroke(1)
        strokeWeight(1)
        strokeCap(SQUARE)
        if(self.laser_init_deg > 360):
            self.laser_init_deg = 0
        else:
            self.laser_init_deg += 1
        
    def overRect(self, x, y, w, h):
        return (x-(w/2)) <= mouseX <= (x + (w/2)) and (y-(h/2)) <= mouseY <= (y + (h/2))
        
    def overCircle(self, x, y, diameter):
        distance = dist(x, y, mouseX, mouseY)
        return distance < diameter / 2


        
        

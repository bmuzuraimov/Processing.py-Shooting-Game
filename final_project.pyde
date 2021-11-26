import random as rd
add_library('sound')
add_library('serial')
from robot import Robot
from game import Game

def setup():
    #setup the serial port
    global myPort, serialInArray, serialCount, firstContact, isClicked
    global gun_x, gun_y, gun_bt1, gun_bt2
    portIndex = 0
    LF = 10
    serialInArray = [None] * 4 # Where we'll put what we receive
    serialCount = 0 # A count of how many bytes we receive
    firstContact = False
    
    # load audio files
    global shoot_mp3, background_mp3
    
    # initialize robot for welcome page
    global w_robot, isWRobot
    isWRobot = True
    w_robot = Robot(width/2, (height/2), 0, 0, 0.7, 0.7, 1) 
    w_robot.isShoot = False
    w_robot.isHacked = False
    w_robot.isSpin = True
    
    global r_pos 
    global game, robot_lanes
    
    size(1200,700)
    
    # create game object 
    game = Game()

    #load sounds using Soundfile
    shoot_mp3 = SoundFile(this, 'data/shoot.mp3')
    background_mp3 = SoundFile(this, 'data/background.mp3')
    background_mp3.amp(0.5)

    # object Serial to read incoming data from exteranl device
    try:
        myPort = Serial(this, Serial.list()[portIndex], 115200) # The serial port
        myPort.bufferUntil(LF)
        print('Connected to serial port '+Serial.list()[portIndex])
    except IndexError:
        print('Device is not detected')
    
    r_pos = [[width/2.22, height/1.87, width/10, height/1.8, 0.1, 1.15, 0], [width/1.82, height/1.87, width/1.11, height/1.8, 0.1, 1.15, 8],
                     [width/2.16, height/1.87, width/5.8, height/1.8, 0.1, 1.25, 1], [width/1.86, height/1.87, width/1.20, height/1.8, 0.1, 1.25, 7],
                     [width/2.1, height/1.87, width/3.5, height/1.8, 0.1, 1.30, 2], [width/1.9, height/1.87, width/1.4, height/1.8, 0.1, 1.30, 6],
                     [width/2.05, height/1.87, width/2.6, height/1.8, 0.1, 1.35, 3], [width/1.95, height/1.87, width/1.62, height/1.8, 0.1, 1.35, 5],
                     [width/2, height/1.87, width/2, height/1.8, 0.1, 1.4, 4]]

    robot_lanes = {'0': 0, '1':2, '2':4, '3':6, '4':8, '5':7, '6':5, '7':3, '8':1}
    
def draw():
    global robot_y, scle, game_robots
    global lane_load
    background(255)
    serialEvent()
    if(game.isCalibrationPage):
        game.starting_page_animation()
        game.set_calibration()
        if(isWRobot): 
            w_robot.display(game.bullets) 
        
    elif(game.isStartingPage):
        game.starting_page()
        
    elif(game.isGamePage):
        game.game_page()
        if(background_mp3.isPlaying() == False): 
            background_mp3.play()
        if(not game.isGeneratedRobots):
            for i in range(len(r_pos)):
                game.game_robots.append(Robot(r_pos[i][0], r_pos[i][1], r_pos[i][2], r_pos[i][3], r_pos[i][4], r_pos[i][5], r_pos[i][6]))
                game.game_robots[i].isSpin = True
                game.game_robots[i].isMoving = True
            game.isGeneratedRobots = True
        if(len(game.game_robots)>0):
            for i, robot in enumerate(game.game_robots):
                if(robot.scle > 0.8):
                    robot.isShoot = True
                    robot.isHacked = True
                if(robot.hp <= 0):
                    game.lane_load[robot.lane] = game.lane_load[robot.lane] - 1
                    game.game_robots.pop(i)
                    r1 = game.lane_load.index(min(game.lane_load))
                    game.lane_load[r1] += 1
                    r1 = robot_lanes[str(r1)]
                    r2 = rd.randint(0, 8)
                    game.lane_load[r2] += 1
                    r2 = robot_lanes[str(r2)]
                    game.game_robots.insert(0, Robot(r_pos[r1][0], r_pos[r1][1], r_pos[r1][2], r_pos[r1][3], r_pos[r1][4], r_pos[r1][5], r_pos[r1][6]))
                    game.game_robots[0].isMoving = True
                    game.game_robots.insert(0, Robot(r_pos[r2][0], r_pos[r2][1], r_pos[r2][2], r_pos[r2][3], r_pos[r2][4], r_pos[r2][5], r_pos[r1][6]))
                    game.game_robots[0].isMoving = True
                    game.myscore += 1
                if(robot.isShoot):
                    game.player_hp -= 1
                robot.display(game.bullets)
                
    elif(game.isRecordsPage):
        game.records_page()
        
    elif(game.isEndGame):   
        game.end_game_page()
        background_mp3.stop()
    
    if(game.isSnipe):
        game.draw_snipe(mouseX, mouseY)
           
    
    
def mouseReleased(): 
    global game, isWRobot, w_robot
    if(background_mp3.isPlaying() == False): 
        background_mp3.play()
    if(game.bullets > 0):
        game.inner_rad = 25
        game.outer_rad = 30
        shoot_mp3.play()
    if (False in game.cal_points and not game.isCalibrated):
        for i in range(len(game.cal_points)):
            if game.cal_points[i] == False:
                game.cal_points[i] = True
                break
    if(game.cal_points[-1] and not game.isCalibrated):
        game.isCalibrated = True
        game.isStartingPage = True
        isWRobot = False
        game.cal_start_time = millis()
    
def keyReleased():
  pass
  
def keyPressed():
    if keyCode == LEFT:
        pass

def serialEvent():
    global firstContact, serialCount, gun_x, gun_y, gun_bt1, gun_bt2, isClicked
    #inByte = myPort.read()
    #if(type(inByte) == 'unicode'):
    #    inByte = inByte.encode('utf-8')
    #print(type(inByte))
    """
    if(firstContact == False):
        if(inByte == 'A'):
            myPort.clear(); # clear the serial port buffer
            firstContact = True # you've had first contact from the microcontroller
            myPort.write('A') # ask for more
    else:
        print(inByte)
        if(inByte == 0):
            isClicked = True
        else:
            isClicked = False
        serialInArray[serialCount] = inByte;
        serialCount = serialCount + 1
        if(serialCount > 3):
            gun_x = serialInArray[0]
            gun_y = serialInArray[1]
            gun_bt1 = serialInArray[2]
            gun_bt2 = serialInArray[3]
            # Send a capital A to request new sensor readings:
            myPort.write('A')   
            serialCount = 0 
    """
    

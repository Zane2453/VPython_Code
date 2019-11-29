acceleration = vec(0,0,0)
def Acceleration_O(data):
    global acceleration
    if data != None:
        acceleration.x = data[0]
        acceleration.y = data[1]
        acceleration.z = data[2]
        
orientation = vec(0,0,0)
def Orientation_O(data):
    global orientation
    if data != None:
        orientation.x = data[0]
        orientation.y = data[1]
        orientation.z = data[2]

def setup():
    profile = {
        'dm_name' : 'Ball-Throw',
        'odf_list' : [Acceleration_O, Orientation_O],
    }
    dai(profile)

setup()

freq = 120        # 更新頻率(Hz)
g = 9.8
size = 1
height = 15
dt = 0.01
maxacc = 0
prevacc = 0
angle = 0
posit = 0
isAnimating = False
satisfy = False
oldOrientation = None
variant = vec(0,0,0)
bgflag = 0

# 初始化場景
def scene_init():
    global scene, laba
    scene = canvas(width=800, height=600, background=color.green, center=vector(5, height / 2 + 20, 0))
    floor = box(length=80, height=2, width=10, color=color.black)
    basketwall = box(length=2, height=52, width=10, pos=vector(40, 25, 0))
    basgoal = box(length=2, height=10, width=10, pos=vector(40, 40, 0), color=color.red)
    laba = label(pos=vector(0, 55, 0), text='angle = \nspeed = ', color=color.red)


# def animate():
#     speed = round(max(10, maxacc * 2))
#     ball = sphere(pos=vector(-40 + posit, 15, 0), radius=size, color=color.blue)
#     ball.v = vector(speed * cos(angle * pi / 180), speed * sin(angle * pi / 180), 0)
#     laba.text = 'angle = ' + angle + '\nspeed = ' + speed
#     def clear():
#         global isAnimating, satisfy, maxacc
#         maxacc = 0
#         isAnimating = False
#         satisfy = False
#         scene.background = color.green
#     def toss():
#         if ball.pos.y <= 45 and ball.pos.y >= 35 and ball.pos.x >= 39 and ball.pos.x <= 41:
#             scene.background = color.purple
#         if ball.pos.x > 41 or ball.pos.y < 0 or ball.pos.y > 60:
#             rate(1, clear)
#             ball.visible = False
#             if scene.background == color.green:
#                 scene.background = color.yellow
#         else :
#             rate(1 / dt, toss)
#             ball.pos = ball.pos + ball.v * dt
#             ball.v.y = ball.v.y - g * dt
#     toss()

# 每秒鐘更新顯示數據
scene_init()

cnt = 0
while True:
    rate(1/dt)
    cnt = cnt + 1
    # bg change green
    if cnt > bgflag + (freq*0.5):
        scene.background = color.green
    console.log(cnt,"or=",orientation,"old=",oldOrientation)
    # acceleration
    scalar = sqrt(acceleration.x ** 2 + acceleration.y ** 2 + acceleration.z ** 2)
    if satisfy and not isAnimating:
        if maxacc == 0:
            maxacc = prevacc
        if scalar > maxacc:
            maxacc = scalar
    prevacc = scalar
    # orientation
    if orientation != vec(0,0,0):
        if not oldOrientation:
            console.log("test?")
            oldOrientation = orientation
        else:
            variant.x = orientation.x - oldOrientation.x
            variant.y = orientation.y - oldOrientation.y
            variant.z = orientation.z - oldOrientation.z
            oldOrientation = vec(orientation.x,orientation.y,orientation.z)
            console.log(cnt,"variant=",variant)
            if not isAnimating:
                flipdegree = min(abs(variant.y), 360 - abs(variant.y))
                if not satisfy:
                    if flipdegree > 30 and abs(variant.z) < 40:
                        satisfy = True
                else:
                    if flipdegree < 10:
                        isAnimating = True
                        angle = round(90 - abs(orientation.y))
                        speed = round(max(10, maxacc * 2))
                        ball = sphere(pos=vector(-40 + posit, 15, 0), radius=size, color=color.blue)
                        ball.v = vector(speed * cos(angle * pi / 180), speed * sin(angle * pi / 180), 0)
                        laba.text = 'angle = ' + angle + '\nspeed = ' + speed
    # toss
    if isAnimating == True:
        if ball.pos.y <= 45 and ball.pos.y >= 35 and ball.pos.x >= 39 and ball.pos.x <= 41:
            scene.background = color.purple
        if ball.pos.x > 41 or ball.pos.y < 0 or ball.pos.y > 60:
            # clear
            maxacc = 0
            isAnimating = False
            satisfy = False
            scene.background = color.green
            ball.visible = False
            if scene.background == color.green:
                scene.background = color.yellow
                bgflag = cnt
        else :
            ball.pos = ball.pos + ball.v * dt
            ball.v.y = ball.v.y - g * dt
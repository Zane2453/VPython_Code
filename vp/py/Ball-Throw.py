g = 9.8
size = 1
height = 15
dt = 0.01
spd = 45
posit = 0
isAnimating = False
oldOrientation = None

def scene_init():
    global scene, laba
    scene = canvas(width=800, height=600, background=color.green, center=vector(5, height / 2 + 15, 0))
    floor = box(length=80, height=2, width=10, color=color.black)
    basketwall = box(length=2, height=52, width=10, pos=vector(40, 25, 0))
    basgoal = box(length=2, height=10, width=10, pos=vector(40, 40, 0), color=color.red)
    laba = label(pos=vector(0, 50, 0), text='angle = ', color=color.red)

def animate():
    angle = 20 + round(random() * 20)
    ball = sphere(pos=vector(-40 + posit, 8, 0), radius=size, color=color.blue)
    ball.v = vector(spd * cos(angle * pi / 180), spd * sin(angle * pi / 180), 0)
    laba.text = 'angle = ' + angle
    def toss():
        global isAnimating
        if ball.pos.y <= 45 and ball.pos.y >= 35 and ball.pos.x >= 39 and ball.pos.x <= 41:
            scene.background = color.purple
        if ball.pos.x > 41 or ball.pos.y < 0:
            ball.visible = False
            scene.background = color.green
            isAnimating = False
        else :
            rate(1 / dt, toss)
            ball.pos = ball.pos + ball.v * dt
            ball.v.y = ball.v.y - g * dt
    toss()

def Orientation_O(data):
    variant = vec(0, 0, 0)
    if data != None:
        global isAnimating, oldOrientation
        if !oldOrientation:
            oldOrientation = vec(data[0], data[1], data[2])
        else:
            variant.x = data[0] - oldOrientation.x
            variant.y = data[1] - oldOrientation.y
            variant.z = data[2] - oldOrientation.z
            oldOrientation = vec(data[0], data[1], data[2])
            flipdegree = min(abs(variant.y), 360 - abs(variant.y))
            if flipdegree > 60 and abs(variant.z) < 25:
                if not isAnimating:
                    isAnimating = True
                    animate()

def setup():
    scene_init()
    profile = {
        'dm_name' : 'Ball-Throw',
        'odf_list' : [Orientation_O],
    }
    dai(profile)

setup()

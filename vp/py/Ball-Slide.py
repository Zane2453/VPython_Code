orientation = vec(0,0,0)
def Orientation_O(data):
    global orientation
    if data != None:
        orientation.x = data[0]
        orientation.y = data[1]
        orientation.z = data[2]
        

# 設定
def setup():
    profile = {
        'dm_name' : 'Ball-Slide',
        'odf_list' : [Orientation_O],
    }
    dai(profile)

setup()


L = 4.9
size = 0.2
dt = 0.01
deg = 10
g = 9.8
count = 0
isAnimating = False
loop_roll = True

def setBoard():
    T2.text = 'Angle: ' + str(abs(deg))
    th = min(abs(deg) * pi / 180, 90 * pi / 180)
    board.pos = vector(-L * cos(th) / 2 - size * sin(th), L * sin(th) / 2 - size * cos(th), 0)
    board.axis = vector(-L * cos(th), L * sin(th),0)


# 初始化場景
def scene_init():
    global scene, board, T2, floor2, floor3
    global L, size
    scene = display(width=900, height=600, background=vector(0.3,0.4,0.4),
                   forward=vector(-0.00963755, -0.266731, -0.963723), center=vector(12, 0, 0))
    board = box(length=L, height=0.05, width=1, pos=vector(-L / 2, -size, 0), axis=vector(-L, 0, 0), color=color.yellow)
    floor1 = box(length=18, height=0.1, width=1.5, color=color.green, pos=vector(8, -10, 0))
    floor2 = box(length=6, height=0.1, width=1.5, color=color.red, pos= vector(20, -10, 0))
    floor3 = box(length=6, height=0.1, width=1.5, color=color.green, pos= vector(26, -10, 0))
    T1 = label(text='Please set the angle in 10~70 degree.\n After setting the angle, please keep it for a while to let the ball release', pos=vector(12, 9, 0), height=20)
    T2 = label(text='Angle: 0', pos = vector(18, 6, 0), height=20)
    

scene_init()

while True:
    rate(1 / dt)
    if not isAnimating:
        if round(orientation.y) == deg:
            count += 1
        else:
            deg = round(orientation.y)
            count = 0
            setBoard()
        if count == 100 and abs(deg) >= 10 and abs(deg) <= 70:
            isAnimating = True
            th = min(abs(deg) * pi / 180, 90 * pi / 180)
            ball = sphere(pos=vector(-L * cos(th), L * sin(th), 0), radius=size, color=color.blue, make_trail=True)
            ball.velocity = vector(0.0, 0.0, 0.0)
            loop_roll = True
    else:
        if loop_roll:
            if ball.pos.y < 0:
                loop_roll = False
            else:
                a = vector(g * sin(th) * cos(th), - g * sin (th) * sin(th), 0)
                ball.velocity = ball.velocity + a * dt                                            
                ball.pos = ball.pos + ball.velocity * dt
        else:
            if ball.pos.x >= floor3.pos.x + floor3.length / 2:
                scene.background = vector(0.3, 0.4, 0.4)
                ball.visible = False
                ball.clear_trail()
                isAnimating = False
            else:
                ball.pos = ball.pos + ball.velocity * dt
                if (ball.pos.x < floor2.pos.x + floor2.length / 2 and ball.pos.x > floor2.pos.x - floor2.length / 2) and ball.pos.y < floor2.pos.y + size + floor2.height / 2:
                    scene.background = vector(0, 0, 0)
                if ball.pos.y < floor2.pos.y + size + floor2.height / 2 and ball.velocity.y < 0:
                    ball.velocity.y = - ball.velocity.y
                else:
                    ball.velocity.y = ball.velocity.y - g * dt
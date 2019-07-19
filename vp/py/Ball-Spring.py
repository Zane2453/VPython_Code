g = 9.8
r = 0.5
spring_coef = 10
dt = 0.01
phoneside = 0
change_flag = True
index = 0

def scene_init():
    global ball, spring, init_value_box
    scene = canvas(width=700, height=600, background=vec(0.6, 0.3, 0.2), range=1.5)
    ceiling = box(length=0.8, height=0.005, width=0.8, color=color.green, pos=vec(0, 0.75, 0))
    ball = sphere(radius=0.05, color=color.white, pos=vec(0, -2 * r + 0.75, 0))
    spring = helix(radius=0.02, thickness=0.02, center=vec(0, 0, 0), axis=vec(0, -1, 0), pos=vec(0, 0.75, 0))
    init_value_box = label(pos=vec(-1.7, 1.2, 0),
                           text='Spring_Constant:\n\nMass:',
                           height=20, border=10, font='monospace',
                           color=color.white, xoffset=1)
    laba = label(pos=vec(0.5, 1.4, 0), text='Flip the smartphone to change the ball mass')
    c = 1
    d = 2
    a = -0.5
    b = -1.25
    arrow(pos=vec(a, b, 0), axis=vec(c + 0.2, 0, 0), shaftwidth=0.015)
    arrow(pos=vec(a, b, 0), axis=vec(0, d + 0.2, 0), shaftwidth=0.015)

    for t in range(0, 5):
        box(pos=vec(a + (t + 1) * (4 / 20), b + d / 2, 0), length=0.005, height=d, width=0.01)

    for j in range(0, 10):
        box(pos=vec(a + c / 2, b + (j + 1) * (d / 10), 0), length=c, height=0.005, width=0.01)

    for x in range(0, 3):
        label(pos=vec(a + x * (c / 5) * 2, b - 2 * d / 20 + 0.1, 0),
              text=str(round(a + x * (c / 5) * 2 * 100) / 100),
              height=20, border=10, font='monospace', box=False)

    for y in range(0, 6):
        label(pos=vec(a - 2 * c / 40 - 0.1, b + y * (d / 5), 0),
              text=str(round(b + y * (d / 5) * 100) / 100 + 0.01),
              height=20, border=10, font='monospace', box=False)

def draw():
    global change_flag
    masses = [0.1, 0.2, 0.3]
    colors = [color.yellow, color.red, color.blue]

    if change_flag is True:
        change_flag = False
        ball.pos0 = vec(0, -2 * r + 0.75, 0)
        ball.pos = vec(0, -2 * r + 0.75, 0)
        ball.v = vec(0, 0, 0)
        ball.a = vec(0, 0, 0)
        ball.mass = masses[index]
        ball.color = colors[index]
        init_value_box.text = 'Spring_Constant: 10\n\nMass: ' + str(ball.mass)
    ball.a = vec(0, spring_coef * (ball.pos0.y - ball.pos.y) / ball.mass - g, 0)
    spring.axis = ball.pos - spring.pos
    ball.v = ball.v + ball.a * dt
    ball.pos = ball.pos + (ball.v) * dt
    rate(1 / dt, draw)

def Orientation_O(data):
    orientation = vec(0, 0, 0)
    if data != None:
        global phoneside, change_flag, index
        orientation.x = data[0]
        orientation.y = data[1]
        orientation.z = data[2]
        if abs(orientation.y) <= 20 and abs(orientation.z) <= 20 and phoneside == 1:
            phoneside = 0
            index = (index + 1) % 3
            change_flag = True
        if abs(orientation.y) >= 160 and abs(orientation.y) <= 180 and abs(orientation.z) <= 20 and phoneside == 0:
            phoneside = 1
            index = (index + 1) % 3
            change_flag = True

def setup():
    scene_init()
    profile = {
        'dm_name' : 'Ball-Spring',
        'odf_list' : [Orientation_O],
    }
    dai(profile)

setup()
draw()

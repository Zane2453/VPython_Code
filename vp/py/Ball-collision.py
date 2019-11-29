acceleration = vec(0,0,0)
scalar = 0
def Acceleration_O(data):
    global acceleration
    if data != None:
        acceleration.x = data[0]
        acceleration.y = data[1]
        acceleration.z = data[2]

def setup():
    profile = {
        'dm_name' : 'Ball-collision',
        'odf_list' : [Acceleration_O],
    }
    dai(profile)

setup()

freq = 120        # 更新頻率(Hz)

# 初始化場景
isAnimating = False
dt = 0.001
freq = 1 / dt

def scene_init():
    global ironball, ping_pong, init_value_box
    scene = canvas(width=900, height=500, background=vector(0.5, 0.6, 0.5), center=vector(0, 0.5, 0))
    arrow1 = arrow(pos=vector(-1, 0.1, 0), axis=vector(2, 0, 0), shaftwidth=0.005)
    ironball = sphere(radius=0.05, pos=vector(-0.8, 0.1, 0), color=vector(0.5, 0.5, 0.5)) 
    ironball.m = 0.5
    ping_pong = sphere(radius=0.02, pos=vector(-0.5, 0.1, 0), color=color.orange)
    ping_pong.m = 0.1
    init_value_box = label(pos=vec(0, 1, 0),
                       text='push the smartphone to start the animation\nironball speed:0\npingpong speed:0',
                       height=20, border=10, font='monospace',
                       color=color.white)

scene_init()

def refresh_text():
    global init_value_box
    init_value_box.text = 'push the smartphone to start the animation\nironball speed:' + str(round(ironball.v * 100) / 100) + '\npingpong speed:' + str(round(ping_pong.v * 100) / 100)

ping_pong.v = 0
ironball.v = 0
while True:
    rate(freq)
    refresh_text()
    scalar = sqrt(acceleration.x ** 2 + acceleration.y ** 2 + acceleration.z ** 2)
    if not isAnimating and scalar > 8:
        isAnimating = True
        ironball.v = 0.8 + 0.02 * (scalar - 8)
        ping_pong.v = 0
    if isAnimating:
        if ping_pong.pos.x > 0.9:
            ironball.pos = vector(-0.8, 0.1, 0)
            ping_pong.pos = vector(-0.5, 0.1, 0)
            #init_value_box.text = 'push the smartphone to start the animation\nironball speed:0\npingpong speed:0'
            isAnimating = False
        else:
            ironball.pos.x = ironball.pos.x + ironball.v * dt
            ping_pong.pos.x = ping_pong.pos.x + ping_pong.v * dt
            if abs(ironball.pos.x - ping_pong.pos.x) < (ironball.radius + ping_pong.radius) and ironball.v > ping_pong.v:
                m_add = ironball.m + ping_pong.m
                m_sub = ironball.m - ping_pong.m
                ironball.v = ironball.v * m_sub / m_add + ping_pong.v * 2 * ping_pong.m / m_add
                ping_pong.v = ironball.v * 2 * ironball.m / m_add - ping_pong.v * m_sub / m_add

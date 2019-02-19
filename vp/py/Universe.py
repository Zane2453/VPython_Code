# 物理參數區
ball_radius = 0.8 # 球半徑(m)
height = 15.0     # 初始高度(m)
speed = 9.8        # 初始速度
gravity = 9.8          # 萬有引力常數
direction = vec(1,0,0) # 初始方向

# 模擬實驗參數區
freq = 240        # 更新頻率(Hz)
dt = 1.0 / freq   # 更新間隔(second)
# 事件旗標區
reset_flag = False
start_flag = False

def scene_init():
    global scene, ball, floor, height, ball_radius, label_gravity
    scene = display(width=800, height=700, center = vec(0, 0, 0), background=vec(0.5, 0.5, 0))
    label_gravity = label( pos=vec(0.8*height,0.8*height,0), text='Gravity: {:.3f}\nSpeed: {:.3f}'.format(gravity,speed))
    floor = sphere(
        pos = vec(0, 0, 0), 
        radius = 2*ball_radius,
        velocity = vec(0, 0, 0)
    )
    ball = sphere(
        pos = vec(0, height, 0), 
        radius = ball_radius,
        velocity = speed*norm(direction)
    )
    scene.autoscale = False
    
    ball.pos.x = 0.0
    ball.pos.y = height * 0.8
    ball.pos.z = 0.0     
    ball.color = color.red
    floor.color = color.green
    
def reset_ball():
    global ball, reset_flag
    # 復位
    ball.pos = vec(0, height, 0)
    # 速度歸零
    ball.velocity = speed*norm(direction)
    # 洗去旗標
    reset_flag = False
    
def Gravity(data):
    global gravity, reset_flag, start_flag
    if data != None and data[0] != gravity:
        reset_flag = True
        gravity = data[0]
        if not start_flag:
            start_flag = True
            animate()
def Speed(data):
    global speed, reset_flag, start_flag
    if data != None and data[0] != gravity:
        reset_flag = True
        speed = data[0]        
        if not start_flag:
            start_flag = True
            animate()
def setup():
    scene_init()
    profile = {
        'dm_name' : 'Universe',
        'odf_list' : [Speed, Gravity]
    }	
    dai(profile)

setup()

def animate():
    global ball, label_gravity
    label_gravity.text = 'Gravity: {:.3f}\nSpeed: {:.3f}'.format(gravity,speed)
    # 模擬天體運動
    if (ball.pos-floor.pos).mag > floor.radius+ball_radius and ball.pos.mag < height*2:
        ball.pos = ball.pos + ball.velocity * dt
    ball.velocity = ball.velocity - gravity * norm(ball.pos - floor.pos) / (ball.pos - floor.pos).mag2
    if reset_flag == True:
        reset_ball()
    rate(freq,animate)

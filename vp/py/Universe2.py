def Speed(data):
    global speed
    if data != None:
        speed = data[0]


# 設定
def setup():
    profile = {
        'dm_name' : 'Universe2',
        'odf_list' : [Speed],
    }
    dai(profile)

setup()

moon_radius = 0.8 # 球半徑(m)
height = 12.0     # 初始高度(m)
speed = 5.5        # 初始速度
gravity = 9.8          # 萬有引力常數
direction = vec(1,0,0) # 初始方向

# 模擬實驗參數區
freq = 120        # 更新頻率(Hz)
dt = 1.0 / freq   # 更新間隔(second)

# 事件旗標區
reset_flag = False

# 重置
def reset_moon():
    global moon, reset_flag
    # 復位
    moon.pos = vec(0, height, 0)
    # 速度歸零
    moon.velocity = speed*norm(direction)
    # 洗去旗標
    reset_flag = False

# 初始化場景
def scene_init():
    global scene, moon, earth, height, moon_radius, label_gravity
    scene = display(width=800, height=700, center = vec(0, -2, -40), background=vec(0, 0, 0))
#    scene = display(width=800, height=700, center = vec(0, -2, -40), background=color.white)
    label_gravity = label( pos=vec(17,15,0), height=20, text='Gravity: {:.3f}\nSpeed: {:.3f}'.format(gravity,speed))
    

    earth = sphere(
        pos = vec(0, 0, 0), 
        radius = 2*moon_radius,
        velocity = vec(0, 0, 0),
        texture = {'file': "/images/earth.jpg"},
        emissive = True,
        opacity = 0.8,

    )
    moon = sphere(
        pos = vec(0, height, 0), 
        radius = moon_radius,
        texture = {'file': "/images/moon.jpg"},
        velocity = speed*norm(direction),
    )

    scene.autoscale = False

scene_init()

#用來判斷萬有引力常數、速度是否改變
prev_state = (gravity, speed)
while True:
    rate(freq)
    label_gravity.text = 'Gravity: {:.3f}\nSpeed: {:.3f}'.format(gravity,speed)
    # 模擬天體運動
    # 模擬天體運動
    if (moon.pos-earth.pos).mag > earth.radius+moon_radius:
        moon.pos = moon.pos + moon.velocity * dt
    
    moon.velocity = moon.velocity - gravity * norm(moon.pos - earth.pos) / (moon.pos - earth.pos).mag2
    #如果萬有引力常數、速度已改變，重置畫面
    if prev_state != (gravity, speed):
        reset_flag = True
    if reset_flag == True:
        reset_moon()
    prev_state = (gravity, speed)

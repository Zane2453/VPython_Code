Station_Humidity = 40
def Weather_Station_Humidity(data):
    global Station_Humidity
    if data != None:
        Station_Humidity = data[0]
        if Station_Humidity < 100:
        	create_tree((Station_Humidity//10)+1)
        else:
            create_tree((Station_Humidity-1//10)+1)
        
Station_Luminance = 50
def Weather_Station_Luminance(data):
    global Station_Luminance, scene
    if data != None:
        Station_Luminance = data[0]
        Change_background(Station_Luminance)
        '''if Station_Luminance <= 40:
            scene.background = vector(0, 0, 0)
        elif Station_Luminance <=60:
            scene.background=vector(0.8156, 0.4647, 0)
        else:
            scene.background=vector(0.4705, 0.6667, 0.8314)'''
        #sun.opacity = Station_Luminance/100
        
# 設定
def setup():
    profile = {
        'dm_name' : 'Weather_Station',
        'idf_list': [],
        'odf_list' : [[Weather_Station_Humidity, ['']], [Weather_Station_Luminance, ['']]],
    }
    dai(profile)

setup()



# [[Weather_Station_Humidity, ['']]] 讀取感測器後會自動更新
# 請勿修改上方程式碼
# https://www.wired.com/story/how-to-make-a-tree-with-fractals/

freq = 50        # 更新頻率(Hz)
tree_sample = []
tree_object = []
iteration = 0

# 初始化場景
def scene_init():
    global label_info, scene
    scene = display(width=800, height=700, center = vector(0, 0, 0), background=vector(0, 0, 0), autoscale = False, range=230)
    scene.lights=[distant_light(direction=vec( 0, 3.7, 4), color=color.gray(0.8)),
 					distant_light(direction=vec(0, -1, -2), color=color.gray(0.3))]
    label_info = label( pos=vec(150,150,0), text='')

# 每秒鐘更新顯示數據
def update_info():
    global label_info, Station_Humidity, Station_Luminance
    label_info.text='Weather_Station_Humidity: {:.2f}\n Weather_Station_Luminance: {:.2f}'.format(Station_Humidity, Station_Luminance)

scene_init()

def Norm(a):
    return vector(-a.y, a.x, 0)
        
def tree(limblen,r,a):
  global tree_sample
  #theta is the "bend angle" for each branching
  theta=30*pi/180
  #short is the amount each branch decreases by
  short=15 #this is the amount each branch is decreased by
  fract=.75
  #repeat the branching until the length is shorter than 5
  if limblen>5:
    tree_sample.append([limblen, r, a])
    #each branch is a cylinder
    #a is a vector that points in the direction of the branch
    tcolor=vector(100,42,42).hat
    if limblen<10:
      tcolor=color.green
    '''cylinder(pos=r,axis=a*limblen, radius=0.15*limblen, 
    color=tcolor, texture=textures.rough)'''
    #r is the position of the next branch
    r=r+a*limblen
    #rotate turns the pointing direction
    a_temp=rotate(a, angle=theta, axis=Norm(a))
    #here is the recursive magic
    tree(limblen*fract,r,a_temp)
    #now you have to go back to where you were
    a_temp=rotate(a_temp, angle=120*pi/180, axis=a)
    #this does the otherside (also recursive)
    tree(limblen*fract,r,a_temp)
    
    a_temp=rotate(a_temp, angle=120*pi/180, axis=a)
    tree(limblen*fract,r,a_temp)
    

#this starts the tree with the starting branchlength = 75
startingbranch=75

#this is the location of the base
startingposition=vector(0,-150,0)

#this is the direction of the first branch (up)
startingdirection=vector(0,1,0)
tree(startingbranch, startingposition, startingdirection)

for i in range(10):
    for j in range(29524):
        if tree_sample[j][0] == startingbranch * (0.75**i):
            tree_object.append(cylinder(
                pos=tree_sample[j][1],
                axis=tree_sample[j][2]*tree_sample[j][0],
                radius=0.15*tree_sample[j][0], 
                color=vector(100,42,42).hat if i<8 else color.green,
                texture=textures.rough,
                visible = False
                ))

create_tree((Station_Humidity//10)+1)

def create_tree(humiduty_rate):
    for i in range(29524):
        tree_object[i].visible = False
    for i in range((3**humiduty_rate - 1)/2):
        tree_object[i].visible = True

sun_light = local_light(pos = vec(-1600, 1600, 0),color=color.white)
#more_sun_light = local_light(pos = vec(-150, 150, 0),color=color.white)

'''sun = sphere(
        pos = vec(-150, 150, 0), 
        radius = 20,
        texture = {'file': "/static/img/sun.jpg"},
        emissive = True,
        opacity = Station_Luminance/100,
    )'''
        
earthOmega = 2*3.14159/356
ground = box(length=1600, 
             height=20, 
             width=1600, 
             pos=vector(0, -150, 0), 
             texture = {'file': "/static/img/Grass.jpg"})
sky = box(length=1600, 
             height=1600, 
             width=20, 
             pos=vector(0, 650, -800), 
             texture = {'file': "/static/img/黃昏.jpg"})

Change_background(Station_Luminance)

def Change_background(luminance):
    global sky
    if luminance <= 20:
        sky.texture = {'file': "/static/img/深夜.jpg"}
    elif luminance <= 40:
        sky.texture = {'file': "/static/img/剛入夜.jpg"}
    elif luminance <= 60:
        sky.texture = {'file': "/static/img/黃昏.jpg"}
    elif luminance <= 80:
        sky.texture = {'file': "/static/img/下午.jpg"}
    else:
    	sky.texture = {'file': "/static/img/中午.jpg"}

cnt = 0
while True:
    rate(freq)
    #sun.rotate(angle=earthOmega, axis=vector(0,150,0), origin=vec(-150, 150, 0))
    cnt = cnt + 1
    if cnt % (freq // 5) == 0:
        update_info()
Station_Humidity = 40
def Weather_Station_Humidity(data):
    global Station_Humidity
    if data != None:
        Station_Humidity = data[0]
        create_tree((Station_Humidity//10)+1)
        
Station_Luminance = 50
def Weather_Station_Luminance(data):
    global Station_Luminance
    if data != None:
        Station_Luminance = data[0]
        
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

freq = 120        # 更新頻率(Hz)
tree_sample = []
tree_object = []
iteration = 0

# 初始化場景
def scene_init():
    global label_info
    scene = display(width=800, height=700, center = vector(10, 15, 0), background=vector(0.5, 0.5, 0))
    label_info = label( pos=vec(150,150,0), text='')

# 每秒鐘更新顯示數據
def update_info():
    global label_info, Station_Humidity, Station_Luminance
    label_info.text='Weather_Station_Humidity: {:.2f}\n Weather_Station_Luminance: {:.2f}'.format(Station_Humidity, Station_Luminance)

scene_init()
        
def tree(limblen,r,a,i):
  global tree_sample,iteration
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
    a=rotate(a, angle=theta, axis=vector(0,0,1))
    #here is the recursive magic
    tree(limblen*fract,r,a,i+1)
    #now you have to go back to where you were
    a=rotate(a,angle=-2*theta,axis=vector(0,0,1))
    #this does the otherside (also recursive)
    tree(limblen*fract,r,a,i+1)
    a=rotate(a,angle=theta,axis=vector(0,0,1))
    r=r-limblen*a
    

#this starts the tree with the starting branchlength = 75
startingbranch=75

#this is the location of the base
startingposition=vector(0,-150,0)

#this is the direction of the first branch (up)
startingdirection=vector(0,1,0)
tree(startingbranch, startingposition, startingdirection, iteration)

for i in range(10):
    for j in range(1023):
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
    for i in range(1023):
        tree_object[i].visible = False
    for i in range((2**humiduty_rate) -1):
        tree_object[i].visible = True

cnt = 0
while True:
    rate(freq)
    cnt = cnt + 1
    if cnt % (freq // 5) == 0:
        update_info()
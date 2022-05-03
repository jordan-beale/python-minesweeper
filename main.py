import pygame, sys, random as r


#things to fix
#-remove flags properly
#-check for if and then remove flags when revealing number tile
#-add win and loss conditions
#-zeroClear sometimes just doesnt work?


#maths functions
def posGet():
    x=((pygame.mouse.get_pos()[0])//26)
    y=((pygame.mouse.get_pos()[1])//26)
    return x,y

def mineLocation():
    mines=[]
    x=99
    while x!=0:
        a=r.randint(0,29)
        b=r.randint(0,15)
        if a<10:
            a="0"+str(a)
        if b<10:
            b="0"+str(b)
        c=str(a)+str(b)
        if c not in mines:
            mines.append(c)
            x-=1
    return mines

def baseGrid(holder):
    grid=[]
    for i in range(0,30):
        jGrid=[]
        for j in range(0,16):
            jGrid.append(holder)
        grid.append(jGrid)
    return grid

mineLocation=mineLocation()
grid=baseGrid("")

def fullGrid(mineLocation,grid):
    for i in range(0,len(mineLocation)):
        num=mineLocation[i]
        grid[int(str(num[0])+str(num[1]))][int(str(num[2])+str(num[3]))]=10

    for i in range(0,30):
        for j in range(0,16):
            if grid[i][j]!=10:
                mines=0
                for k in range(-1,2):
                    for n in range(-1,2):
                        try:
                            if -1<(i+k)<30 and -1<(j+n)<16:
                                if grid[i+k][j+n]==10:
                                    mines+=1
                        except IndexError:
                            continue
                grid[i][j]=mines
    return(grid)

grid=fullGrid(mineLocation,grid)

#add and remove sprite functions
def removeBlocker(posArray):
    try:
        (blockers[posArray[0]][posArray[1]]).delete((26*posArray[0]+1),(26*posArray[1]+1))
    except IndexError:
        pass

def addNumber(x,y):
    number=General(str(grid[x][y])+".png",(26*(x)+1),(26*(y)+1))
    numbersGroup.add(number)
    grid[x][y]=100

def changeFlag(flags,flagGrid):
    if flagGrid[posGet()[0]][posGet()[1]]==1:
        flags=removeFlag(flags,flagGrid)
    else:
        addFlag(flags,flagGrid)

def removeFlag(flags,flagGrid):
    (flags[posGet()[0]][posGet()[1]]).delete((26*(posGet()[0])+1),(26*(posGet()[1])+1))
    flagGrid[posGet()[0]][posGet()[1]]=0
    return flags,flagGrid
def addFlag(flags,flagGrid):
    flags[posGet()[0]][posGet()[1]]="flag"+str(posGet()[0])+str(posGet()[1])
    flags[posGet()[0]][posGet()[1]]=General("flag.png",(26*(posGet()[0])+1),(26*(posGet()[1])+1))
    flagGroup.add(flags[posGet()[0]][posGet()[1]])
    flagGrid[posGet()[0]][posGet()[1]]=1
    return flags,flagGrid

def zeroClear(x,y):
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                if grid[x+i][y+j]==0:
                    removeBlocker([(x+i),(y+j)])
                    grid[x+i][y+j]=9
                    zeroClear(x+i,y+j)
                elif 0<grid[x+i][y+j]<9:
                    removeBlocker([(x+i),(y+j)])
                    addNumber((x+i),(y+j))
            except IndexError:
                pass
                

def gameOver():
    mine=General("mine.png",(26*(posGet()[0])+1),(26*(posGet()[1])+1))
    numbersGroup.add(mine)
    
def leftclick():
    try:
        if grid[posGet()[0]][posGet()[1]] == 0:
            zeroClear(posGet()[0],posGet()[1])
        elif grid[posGet()[0]][posGet()[1]] == 10:
            gameOver()
        elif 0<grid[posGet()[0]][posGet()[1]]<9:
            addNumber(posGet()[0],posGet()[1])
    except IndexError:
        pass

#classes
class General(pygame.sprite.Sprite):
    
    def __init__(self,image_path,pos_x,pos_y):
        super().__init__()
        self.image=pygame.image.load(image_path)
        self.rect=self.image.get_rect()
        self.rect.topleft=[pos_x,pos_y]

    def delete(self,x,y):
        if self.rect.collidepoint(x,y):
            self.kill()
        
#setup
pygame.init()
clock=pygame.time.Clock()

#colours
colour_grey_0=(166,167,171)
colour_black=(0,0,0)
colour_white=(255,255,255)

#game screen
screen_width=781
screen_height=417
screen=pygame.display.set_mode((screen_width,screen_height))

#background
def background():
    screen.fill(colour_grey_0)
    a=0
    for i in range(0,31):
        pygame.draw.line(screen,colour_black,(a,0),(a,417),1)
        a=a+26
    b=0
    for i in range(0,17):
        pygame.draw.line(screen,colour_black,(0,b),(781,b),1)
        b=b+26
        

#Groups
numbersGroup=pygame.sprite.Group()
flagGroup=pygame.sprite.Group()
blockerGroup=pygame.sprite.Group()
flagGrid=baseGrid(0)

#blockers
blockers=baseGrid("")
for i in range(0,30):
    for j in range(0,16):
        blockers[i][j]=("fBlocker"+str(i)+str(j))
        blockers[i][j]=General("blocker.png",(26*i+1),(26*j+1))
        blockerGroup.add(blockers[i][j])


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                removeBlocker(posGet())
                leftclick()
            if event.button==3:
                changeFlag(baseGrid(""),flagGrid)
                
    pygame.display.update()        
    background()
    blockerGroup.draw(screen)
    flagGroup.draw(screen)
    numbersGroup.draw(screen)
    clock.tick(60)

    

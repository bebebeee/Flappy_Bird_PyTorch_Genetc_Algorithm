import pygame
pygame.init()
import random
import time
import numpy as np
import math



class birdbody(pygame.sprite.Sprite):
    def __init__(self):
        #print('inted')
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/birdf.png')
        self.rect = self.image.get_rect()
        self.rect.center = [300,500]
        self.velocityup = 0

    def jump(self):
        self.velocityup -= 1
        self.checkvels()
        self.rect.y += self.velocityup
       

    def fall(self):
        self.velocityup += 0.05
        #print(str(self.velocityup))
        self.checkvels()
        self.rect.y += self.velocityup

    def checkvels(self): #if velocitty is toooo big
        if self.velocityup>=2:
            #print(str(self.velocityup))
            self.velocityup = 2
        elif self.velocityup <= -1.6:
            #print('b')
            self.velocityup = -1.6
        if self.rect.y >= 950:
            #print('c')
            self.rect.y = 950
            self.velocityup = 0
        elif self.rect.y <= 0:
            #print('d')
            self.rect.y = 0
            self.velocityup = 0

         
class birdbrain():
    def __init__(self):
        #print('inited')
        self.brainl1 = 2*np.random.random((4,3))-1 #nural newtork: self height, distance from lower, distance from heighter
        self.brainl2 = 2*np.random.random((3,4))-1 #hidden two layers
        self.brainl3 = 2*np.random.random((4,1))-1 #last layer -- jump or not!!
        self.bias = 0.2*np.random.random((1,1))-0.1
        self.controlbody = birdbody()
       

    def makemove(self,infolist): #infolist is a numpy array [,,]
        hidden1 = self.relu(np.dot(infolist,self.brainl1))
        hidden2 = self.relu(np.dot(hidden1,self.brainl2))
        results = self.relu(np.dot(hidden2,self.brainl3))
        results = np.add(results,self.bias)
        if results >= 0.25:
            self.controlbody.jump()

    def relu(self,x):
        return np.maximum(0,x)
         


class gamerun():
    def __init__(self,basics = None):
        self.window = pygame.display.set_mode([1500,1000])
        self.window.fill((135,206,235))
        self.breakq = False
        pygame.display.update()
        self.colist = [] #list of all the bars
        self.createcol() #create a new 'bar'
        self.timestamp = 0 #timestamp keep track
        self.level = 0
        self.mybirdis = pygame.sprite.Group()
        #basicly, this generates the random birdies 
        self.mutatera = 0.05
        self.si = 0.97
        self.birdbrain = []
        for _ in range(600): #this is the number of trials birds
            self.birdbrain.append(birdbrain())
        self.mybirdi = []

        if basics == None:
            for bn in self.birdbrain:
                self.mybirdi.append(bn.controlbody)
                self.mybirdis.add(bn.controlbody)

        else:
            for bn in self.birdbrain:
                m1 = self.mutatera*np.random.random((4,3))-self.mutatera/2
                m2 = self.mutatera*np.random.random((3,4))-self.mutatera/2
                m3 = self.mutatera*np.random.random((4,1))-self.mutatera/2
                bas = 0.01*np.random.random((1,1))-0.005
                bn.brainl1 = np.add(basics[0],m1) #FIX LATER FIND CLOSEST TARGETTT
                bn.brainl2 = np.add(basics[1],m2)
                bn.brainl3 = np.add(basics[2],m3)
                bn.bias = np.add(basics[3],bas)
                #add bird to lists
                self.mybirdi.append(bn.controlbody)
                self.mybirdis.add(bn.controlbody)

        self.infosheet = open("infosheet.txt","w")
        
        while self.breakq == False: #main loop
            self.timestamp += 1
            self.runframe()
            self.mybirdis.draw(self.window)
            pygame.display.update()
 
    def trnbreakfal(self):
        self.breakq = True

    def createcol(self):
     
        firrand = random.randint(300,700) #genterate random pos for bars
        #each time frame, every rectangular in colist will move left
        randup = random.choices([-1,1], weights = [1,1], k=1)
        self.colist.append([firrand,firrand+150,0,None,[None,None],randup[0]]) #first two are starts and stops of bar and last is the time this is made
        self.createcolbased(firrand,firrand+150)

    def createcolbased(self,coord1,coord2):
        #drawing bars
        #self.colist[len(self.colist)-1][3] = 1500-100#this is the x positon of this rectanglular
        #x is the x coords of the bars
        self.colist[-1][3] = 1400
        self.colist[-1][4][0] = pygame.draw.rect(self.window, (0,0,0), (1400,0,80,1000-coord2))
        self.colist[-1][4][1] = pygame.draw.rect(self.window, (0,0,0), (1400,1000-coord1,80,coord1))
        

    def runframe(self):
        #Basic things -------------------------------------------------------------------
        for event in pygame.event.get(): #break game
            if event.type == pygame.QUIT:
                self.infosheet.write(str(self.lastbest.brainl1)+ '|' +str(self.lastbest.brainl2)+ '|'+str(self.lastbest.brainl3)+ '|'+ str(self.lastbest.bias)+'____')
                self.breakq = True
        self.window.fill((135,206,235)) #draw over everything
        #time.sleep(0.0002)
        #handleing bars --------------------------------------------------------------
        deltebars = []
        for colpairs in self.colist: #move existing rects
            #pygame.draw.rect(self.window,(135,206,235),colpairs[4][0]) #draw over rects to 'delete' so stupicl
            #pygame.draw.rect(self.window,(135,206,235),colpairs[4][1]) #draw over rects to 'delete'
            colpairs[2] -= 0.7 #new pos speed or difficulty1-1-1-1-1-1--1--1111!!!!!!!!!!~!~

            if colpairs[0] <= 30 or colpairs[1] >= 970: #verdicle challenges
                colpairs[5] *= -1
            if colpairs[5]==1:
                colpairs[0] += 1.2+self.si #verdicle challenges
                colpairs[1] += 1.2+self.si
            else:
                colpairs[0] -= 1.2+self.si #verdicle challenges
                colpairs[1] -= 1.2+self.si
            if colpairs[2] <= -1200: #delete if out
                self.level += 1
                self.si += 0
                print(str(self.level))
                deltebars.append(colpairs)
            else:
                colpairs[4][0] = pygame.draw.rect(self.window,(0,0,222),(colpairs[2]+1400,0,80,1000-colpairs[1]))
                colpairs[4][1] = pygame.draw.rect(self.window, (0,0,222), (colpairs[2]+1400,1000-colpairs[0],80,colpairs[0]))
            #Moving pipes
    #bars complete--------------------------------------------------------------------------------   
            
        for killbar in deltebars: #delete the bars that have gone out
            self.colist.remove(killbar)
        if self.timestamp % 800 == 0: #generate new bars if timestamp intervals
            self.createcol()    
        #dealing with birds -------------------------------------------------------
        birdDeletionList = []
        for bird in self.birdbrain: #bird is actually its brain
            contrbird = bird.controlbody
            #check colisons
            if pygame.Rect.colliderect(contrbird.rect,self.colist[0][4][1]) or pygame.Rect.colliderect(contrbird.rect,self.colist[0][4][0]):
                birdDeletionList.append(bird)
            #movingggsssssssss
            contrbird.fall()
            if self.timestamp % 10 == 0:
                bird.makemove([self.colist[0][0]/250,(self.colist[0][2]+1400-300)/200,contrbird.rect.y/300,self.colist[0][5]*(1.2+self.si)])
                
        for bird in birdDeletionList: #delete ones that did not make it
            self.mybirdi.remove(bird.controlbody)
            bird.controlbody.kill()
            self.birdbrain.remove(bird)

        if len(self.birdbrain) == 0: #new generation
            self.si = 0.97
            print(str(self.level))
            
            #generate new birdiesss!
            
            self.birdbrain = []
            for _ in range(250): #this is the number of trials birds
                self.birdbrain.append(birdbrain())
            
            bestdiss = 9999
            self.lastbest = None
            secondbest = None
            #find best birdie
            for bird in birdDeletionList:
                diss = abs(bird.controlbody.rect.y-self.colist[0][0]-75)
                if diss<bestdiss:
                    bestdiss = diss
                    secondbest = self.lastbest
                    self.lastbest = bird
            if secondbest == None:
                secondbest = self.lastbest
    
            self.mutatera = 0.25*(0.9)**self.level
            self.mybirdi = []
            for bn in self.birdbrain:
                #alter the brain
                
                m1 = self.mutatera*np.random.random((4,3))-self.mutatera/2
                m2 = self.mutatera*np.random.random((3,4))-self.mutatera/2
                m3 = self.mutatera*np.random.random((4,1))-self.mutatera/2
                bas = 0.01*np.random.random((1,1))-0.005
                bn.brainl1 = np.add(self.lastbest.brainl1,m1) #FIX LATER FIND CLOSEST TARGETTT
                bn.brainl2 = np.add(secondbest.brainl2,m2)
                bn.brainl3 = np.add(self.lastbest.brainl3,m3)
                bn.bias = np.add(secondbest.bias,bas)
                #add bird to lists
                self.mybirdi.append(bn.controlbody)
                self.mybirdis.add(bn.controlbody)
            self.level = 0
            self.colist.pop(0) #buy time

    
        
  



brainlist = [np.array([[-0.23220791,  0.61394487, -0.91529679],
 [-0.63126184, -0.0131258,   0.16323777],
 [-0.13223944,  0.83355946,  0.10904688],
 [-0.0654954,   0.0271203,   0.10792209]]),np.array([[ 0.38051445,  0.55804905,  0.80010187, -0.00719983],
 [-0.37314002,  0.74597081, -1.12701357, -0.74268353],
 [ 0.98510888,  1.42074389, -0.92418593,  0.76349566]]), np.array([[ 1.04240024],
 [ 0.16909657],
 [ 0.95856323],
 [-0.70040582]]), np.array([[-0.05104436]])]   
mygame = gamerun(basics = brainlist)

pygame.quit()


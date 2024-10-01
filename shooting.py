import pygame
import random 
import math
pvelo = 6
psvelo = 2
COLORS = [[255,0,0],[100,255,100],[255,0,0],[255,255,0],[0,255,255],[0,0,255],[128,0,128],[200,200,200],[0,255,0]]
pygame.init()      
screen = pygame.display.set_mode((640, 480)) 

#画像をロード
heart_image = pygame.image.load("images/heart.png")
player_image = pygame.image.load("images/dot_koishi.png") 
enemy1_image = pygame.image.load("images/dot_koakuma.png")
enemy2_image = pygame.image.load("images/dot_rumia.png")
enemy3_image = pygame.image.load("images/dot_cirno.png")
boss_image = pygame.image.load("images/dot_alice.png")
back_rough_image1 = pygame.image.load("images/night.jpg")
backimage1 = pygame.transform.scale(back_rough_image1, (640,480))
back_rough_image2 = pygame.image.load("images/moon.jpg")
backimage2 = pygame.transform.scale(back_rough_image2, (640,480))
back_rough_image3 = pygame.image.load("images/noon.jpg")
backimage3 = pygame.transform.scale(back_rough_image3, (640,480))
clock = pygame.time.Clock()

#プレイヤー
class Player:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.rough_image = pygame.image.load("images/dot_koishi.png")
        self.image = pygame.transform.scale(self.rough_image, (40,60))
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.slow = False #低速移動用フラグ
        self.shooting = False #弾幕発射用フラグ
        self.life = 4
        self.life_lost_time = 0
        self.killcount = 0 #撃破数
        self.boss = False #ボス出現フラグ
        self.bosstime1 = 0 #ボス弾幕用変数
        self.bosstime2 = 0
        self.bosstime3 = 0
        self.bosskill = False
    
    #キーの入力に対応する関数
    def update(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move_right = True
            if event.key == pygame.K_LEFT:
                self.move_left = True
            if event.key == pygame.K_UP:
                self.move_up = True
            if event.key == pygame.K_DOWN:
                self.move_down = True
            if event.key == pygame.K_LSHIFT:
                self.slow = True
            if event.key == pygame.K_z:
                self.shooting = True        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_LEFT:
                self.move_left = False
            if event.key == pygame.K_UP:
                self.move_up = False
            if event.key == pygame.K_DOWN:
                self.move_down = False
            if event.key == pygame.K_LSHIFT:
                self.slow = False     
            if event.key == pygame.K_z:
                self.shooting = False

#プレイヤーの弾幕               
class Bullet:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        self.rough1_image = pygame.image.load("images/kShot.png")
        self.image = pygame.transform.scale(self.rough1_image, (10,10))

    #上に移動
    def update(self):
        self.y -= 20
        screen.blit(self.image,(self.x-5,self.y-5))

    #着弾判定
    def judge(self,enemy):
        if((self.y > (enemy.y-20) and self.y < (enemy.y + 20)) and (self.x > (enemy.x-20) and self.x < (enemy.x + 20))):
            return True            
        else:
            return False

#エネミー1            
class Enemy1:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x_dir = 1
        self.y_dir = 1
        self.life = 50
        self.e_shot1= False
        self.death = False
        self.hiteffect = False
        self.rough_image = pygame.image.load("images/dot_koakuma.png")
        self.image = pygame.transform.scale(self.rough_image, (40,50))

    #移動
    def update(self):
        if(random.randrange(200) < 2):
            self.x_dir = self.x_dir*-1
        if(random.randrange(200) < 5):
            self.y_dir = self.y_dir*-1    
        if self.x < 3 or self.x > 617:
            self.x_dir = self.x_dir*-1
        if self.y < 3 or self.y > 240:
            self.y_dir = self.y_dir*-1
        self.x += 1*self.x_dir
        self.y += 1*self.y_dir
        if(random.randrange(500) < 1):
            self.e_shot1 = True
        else:
            self.e_shot1 = False    

    #被弾            
    def hit(self):
        self.life -= 1
        self.hiteffect = True
        if self.life <= 0:
            self.death = True

#エネミー1の弾幕
class EnemyBullet1:
    def __init__(self,x,y,d):
        self.x = x
        self.y = y
        self.dir = d #角度用変数
        self.rough1_image = pygame.image.load("images/kShot2.png")
        self.image = pygame.transform.scale(self.rough1_image, (16,16)) 

    #移動
    def update(self):
        self.x += 2*math.cos(math.pi/6*self.dir)
        self.y += 2*math.sin(math.pi/6*self.dir)
        screen.blit(self.image,(self.x-8,self.y-8))        

    #着弾判定
    def judge(self,player):
        if((self.y > (player.y-8) and self.y < (player.y + 8)) and (self.x > (player.x -8) and self.x < (player.x + 8))):
            return True            
        else:
            return False

#エネミー2
class Enemy2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x_dir = 1
        self.y_dir = 1
        self.life = 50
        self.e_shot1= False
        self.hiteffect = False
        self.death = False
        self.rough_image = pygame.image.load("images/dot_rumia.png")
        self.image = pygame.transform.scale(self.rough_image, (40,50))


    #移動
    def update(self):
        if(random.randrange(200) < 2):
            self.x_dir = self.x_dir*-1
        if(random.randrange(200) < 5):
            self.y_dir = self.y_dir*-1    
        if self.x < 3 or self.x > 617:
            self.x_dir = self.x_dir*-1
        if self.y < 3 or self.y > 240:
            self.y_dir = self.y_dir*-1
        self.x += 1*self.x_dir
        self.y += 1*self.y_dir
        if(random.randrange(500) < 1):
            self.e_shot2 = True
        else:
            self.e_shot2 = False     
    #被弾           
    def hit(self):
        self.hiteffect = True
        self.life -= 1
        if self.life <= 0:
            self.death = True 

#エネミー2の弾幕
class EnemyBullet2:
    def __init__(self,x,y,d):
        self.x = x
        self.y = y
        self.dir = d
        self.rough1_image = pygame.image.load("images/kShot3.png")
        self.image = pygame.transform.scale(self.rough1_image, (10,10)) 

    #移動
    def update(self):
        self.x += 3*math.cos(math.pi/6*self.dir)
        self.y += 3*math.sin(math.pi/6*self.dir)
        screen.blit(self.image,(self.x-5,self.y-5))

    #着弾判定
    def judge(self,player):
        if((self.y > (player.y-5) and self.y < (player.y + 5)) and (self.x > (player.x -5) and self.x < (player.x + 5))):
            return True            
        else:
            return False  

#エネミー3
class Enemy3:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x_dir = 1
        self.y_dir = 1
        self.life = 50
        self.e_shot1= False
        self.hiteffect = False
        self.death = False
        self.rough_image = pygame.image.load("images/dot_cirno.png")
        self.image = pygame.transform.scale(self.rough_image, (40,50))

    #移動
    def update(self):
        if(random.randrange(200) < 2):
            self.x_dir = self.x_dir*-1
        if(random.randrange(200) < 5):
            self.y_dir = self.y_dir*-1    
        if self.x < 3 or self.x > 617:
            self.x_dir = self.x_dir*-1
        if self.y < 3 or self.y > 240:
            self.y_dir = self.y_dir*-1
        self.x += 1*self.x_dir
        self.y += 1*self.y_dir
        if(random.randrange(500) < 5):
            self.e_shot1 = True
        else:
            self.e_shot1 = False     

    #被弾判定           
    def hit(self):
        self.hiteffect = True
        self.life -= 1
        if self.life <= 0:
            self.death = True                             

#エネミー3の弾幕
class EnemyBullet3:
    def __init__(self,x,y,px,py,ex,ey):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.ex = ex
        self.ey = ey
        self.rough1_image = pygame.image.load("images/kShot4.png")
        self.image = pygame.transform.scale(self.rough1_image, (14,14)) 

    #移動
    def update(self):
        self.x += -4*(self.ex-self.px)/((self.ex-self.px)**2+(self.ey-self.py)**2)**0.5
        self.y += -4*(self.ey-self.py)/((self.ex-self.px)**2+(self.ey-self.py)**2)**0.5
        screen.blit(self.image,(self.x-7,self.y-7))

    #着弾判定
    def judge(self,player):
        if((self.y > (player.y-7) and self.y < (player.y + 7)) and (self.x > (player.x -7) and self.x < (player.x + 7))):
            return True            
        else:
            return False       

#ボス
class BOSS:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x_dir = 1
        self.y_dir = 1
        self.life = 2400
        self.e_shot1= False
        self.e_shot2= False
        self.e_shot3= False
        self.hiteffect = False
        self.death = False
        self.stop = False
        self.rough_image = pygame.image.load("images/dot_alice.png")
        self.image = pygame.transform.scale(self.rough_image, (40,70))

    #移動
    def update(self):
        if(random.randrange(200) < 2):
            self.x_dir = self.x_dir*-1
        if(random.randrange(200) < 5):
            self.y_dir = self.y_dir*-1    
        if self.x < 100 or self.x > 540:
            self.x_dir = self.x_dir*-1
        if self.y < 50 or self.y > 160:
            self.y_dir = self.y_dir*-1
        if self.stop == False:
            self.x += 2*self.x_dir
            self.y += 2*self.y_dir
        #確率で弾幕を発射    
        if(random.randrange(500) < 5 and self.stop == False ):
            self.e_shot1 = True
        if(random.randrange(500) < 5 and self.stop == False ):
            self.e_shot2 = True 
        if(random.randrange(500) < 5 and self.stop == False ):
            self.e_shot3 = True     

    #被弾判定            
    def hit(self):
        self.hiteffect = True
        self.life -= 1
        if self.life <= 0:
            self.death = True 

#ボス弾幕1
class Bossbullet1:
    def __init__(self,x,y,d):
        self.x = x
        self.y = y
        self.dir = d
        self.rough1_image = pygame.image.load("images/kShot5.png")
        self.image = pygame.transform.scale(self.rough1_image, (16,16)) 

    #移動    
    def update(self):
        self.x += 2*math.cos(math.pi/18*self.dir)
        self.y += 2*math.sin(math.pi/18*self.dir)
        screen.blit(self.image,(self.x-8,self.y-8))

    #着弾判定                
    def judge(self,player):
        if((self.y > (player.y-8) and self.y < (player.y + 8)) and (self.x > (player.x -8) and self.x < (player.x + 8))):
            return True            
        else:
            return False

#ボス弾幕2
class Bossbullet2:
    def __init__(self,x,y,px,py,ex,ey):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.ex = ex
        self.ey = ey
        self.rough1_image = pygame.image.load("images/kShot6.png")
        self.image = pygame.transform.scale(self.rough1_image, (14,14))

    #移動
    def update(self):
        self.x += -3*(self.ex-self.px)/((self.ex-self.px)**2+(self.ey-self.py)**2)**0.5
        self.y += -3*(self.ey-self.py)/((self.ex-self.px)**2+(self.ey-self.py)**2)**0.5
        screen.blit(self.image,(self.x-7,self.y-7))

    #着弾判定
    def judge(self,player):
        if((self.y > (player.y-7) and self.y < (player.y + 7)) and (self.x > (player.x -7) and self.x < (player.x + 7))):
            return True            
        else:
            return False    

#ボス弾幕3
class Bossbullet3:
    def __init__(self,x,y,d,bx,by):
        self.x = x
        self.y = y
        self.boss_x = bx
        self.boss_y = by
        self.dir = d
        self.r = 1
        self.rough1_image = pygame.image.load("images/kShot3.png")
        self.image = pygame.transform.scale(self.rough1_image, (16,16)) 

    #移動
    def update(self):
        self.r += 1     
        self.x = self.boss_x+1*self.r*math.cos(math.pi/10*self.dir+math.pi/540*self.r)
        self.y = self.boss_y+1*self.r*math.sin(math.pi/10*self.dir+math.pi/540*self.r)
        screen.blit(self.image,(self.x-8,self.y-8))

    #着弾判定            
    def judge(self,player):
        if((self.y > (player.y-8) and self.y < (player.y + 8)) and (self.x > (player.x -8) and self.x < (player.x + 8))):
            return True            
        else:
            return False

#パーティクル
class Particle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.t = 0

    def update(self):
        self.t += 1
        pygame.draw.circle(screen, COLORS[1], [self.x-random.randint(-3,3), self.y-random.randint(-5,5)], 3)

#撃破時のパーティクル
class Deathparticle:
    def __init__(self,x,y,c):
        self.x = x
        self.y = y
        self.t = 0
        self.color = c
        self.t = 0
    def update(self):
        self.t += 1
        for i in range(0,3):
            pygame.draw.circle(screen, COLORS[self.color], [self.x-random.randint(-15,15), self.y-random.randint(-30,30)], random.randint(3,7))
            pygame.draw.circle(screen, (255,255,255), [self.x-random.randint(-15,15), self.y-random.randint(-30,30)], random.randint(1,5))    

#タイマー
class Timer:
    def __init__(self,T):
        self.time = 0
        self.maxtime = T
        self.t = False

    def update(self):
        self.time += 1
        if self.time > self.maxtime:
            self.t = True

#開始画面            
def open(): 
    endFlag = False
    font1 = pygame.font.SysFont(None, 40)
    text1 = font1.render("[PLAYER]", False, (255,255,255))
    text2 = font1.render("[MOVE]                         ←↑→↓ ",False,(255,255,255))
    text3 = font1.render("[MOVE SLOWLY]     Lshift +  ←↑→↓ ",False,(255,255,255))
    text4 = font1.render("[LAUNCH]                       Z",False,(255,255,255))
    text5 = font1.render("[ENEMY]",False,(255,255,255))
    text6 = font1.render("[BOSS]",False,(255,255,255))
    text7 = font1.render("Press Any Key to Start!!",False,(255,255,255))
   
    while endFlag == False:
        screen.fill((0,0,0))
        screen.blit(backimage1,(0,0))
        screen.blit(text1,(100,50))
        screen.blit(text2,(100,100))
        screen.blit(text3,(100,150))
        screen.blit(text4,(100,200))
        screen.blit(text5,(100,270))
        screen.blit(text6,(100,340))
        screen.blit(text7,(150,400))
        screen.blit(player_image,(400,40))    
        screen.blit(enemy1_image,(340,250)) 
        screen.blit(enemy2_image,(420,250))
        screen.blit(enemy3_image,(500,250)) 
        screen.blit(boss_image,(425,325))  
      
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                endFlag = True
            elif event.type == pygame.KEYDOWN:
                endFlag = True
                main()

#ゲーム開始
def main():
    endFlag = False
    player = Player(320,400)
    time_elapsed = 0
    force_quit = False
    bullets= [] #弾幕を入れる配列
    enemy1s = [] #エネミーを入れる配列
    enemy2s = []
    enemy3s = []
    bosses = [] #ボスを入れる配列
    e_bullets1 = [] #エネミーの弾幕を入れる配列  
    particles = [] #パーティクルを入れる配列
    deathparticles = [] #撃破時パーティクルを入れる配列
    timers = []
    while endFlag == False:
        clock.tick(60) 
        time_elapsed += 1
        screen.fill((0,0,0))
        screen.blit(backimage2,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                endFlag = True
                force_quit = False
            else:
                player.update(event)

        #プレイヤーの移動
        if player.move_right == True:
            if player.x < 620:
                if player.slow == True:
                    player.x += psvelo
                if player.slow == False:
                    player.x += pvelo
        if player.move_left == True:
            if player.x > 00:
                if player.slow == True:
                    player.x -= psvelo
                if player.slow == False:
                    player.x -= pvelo
        if player.move_up == True:
            if player.y > 00:
                if player.slow == True:
                    player.y -= psvelo
                if player.slow == False:
                    player.y -= pvelo
        if player.move_down == True:
            if player.y < 460:
                if player.slow == True:
                    player.y += psvelo
                if player.slow == False:
                    player.y += pvelo

        #弾幕射撃            
        if player.shooting == True:
            b=Bullet(player.x,player.y)
            bullets.append(b)

        #エネミー出現
        if(random.randrange(200) < 1 and player.boss == False):
            e1 = Enemy1(random.randint(5,610),20)
            enemy1s.append(e1) 

        if(random.randrange(200) < 1 and player.boss == False):
            e2 = Enemy2(random.randint(5,610),20)
            enemy2s.append(e2) 

        if(random.randrange(200) < 1 and player.boss == False):
            e3 = Enemy3(random.randint(5,610),20)
            enemy3s.append(e3)

        #プレイヤーの弾幕着弾判定
        for bullet in bullets:
            bullet.update()
            for enemy1 in enemy1s:
                if bullet.judge(enemy1) == True:
                    enemy1.hit()    
            for enemy2 in enemy2s:        
                if bullet.judge(enemy2) == True:
                    enemy2.hit()
            for enemy3 in enemy3s:        
                if bullet.judge(enemy3) == True:
                    enemy3.hit()                    
            for boss in bosses:        
                if bullet.judge(boss) == True:
                    boss.hit()              
            if bullet.y<0:
                bullets.remove(bullet)

        #エネミーの移動と弾幕発射と被弾判定
        for enemy1 in enemy1s:
            enemy1.update()
            if enemy1.e_shot1 == True:
                for i in range(0,13):
                    eb=EnemyBullet1(enemy1.x,enemy1.y,i)
                    e_bullets1.append(eb)
            if enemy1.hiteffect == True:
                ef = Particle(enemy1.x,enemy1.y)  
                particles.append(ef)
                enemy1.hiteffect = False      
            screen.blit(enemy1.image,(enemy1.x-20,enemy1.y-22))
            if enemy1.death == True:
                enemy1s.remove(enemy1)
                de=Deathparticle(enemy1.x,enemy1.y,2)
                deathparticles.append(de)
                player.killcount += 1

        for enemy2 in enemy2s:
            enemy2.update()
            if enemy2.e_shot2 == True:
                for i in range(0,11):
                    eb=EnemyBullet2(enemy2.x,enemy2.y,i)
                    e_bullets1.append(eb)
            if enemy2.hiteffect == True:
                ef = Particle(enemy2.x,enemy2.y)  
                particles.append(ef)
                enemy2.hiteffect = False        
            screen.blit(enemy2.image,(enemy2.x-19,enemy2.y-20))
            if enemy2.death == True:
                enemy2s.remove(enemy2)
                de=Deathparticle(enemy2.x,enemy2.y,3)
                deathparticles.append(de)
                player.killcount += 1 

        for enemy3 in enemy3s:
            enemy3.update()
            if enemy3.e_shot1 == True:
                eb=EnemyBullet3(enemy3.x,enemy3.y,player.x,player.y,enemy3.x,enemy3.y)
                e_bullets1.append(eb)
            if enemy3.hiteffect == True:
                ef = Particle(enemy3.x,enemy3.y)  
                particles.append(ef)
                enemy3.hiteffect = False    
            screen.blit(enemy3.image,(enemy3.x-21,enemy3.y-25))
            if enemy3.death == True:
                enemy3s.remove(enemy3)
                de=Deathparticle(enemy3.x,enemy3.y,4)
                deathparticles.append(de)
                player.killcount += 1

        #ボスの移動と弾幕発射と被弾判定
        for boss in bosses:
            boss.update()
            pygame.draw.rect(screen, (255,100,200), (30,30,boss.life/2400*580,5))
            if boss.e_shot1 == True:
                player.bosstime1 = time_elapsed
                boss.stop = True
                #ボス弾幕1
                for i in range(36):
                    eb=Bossbullet1(boss.x,boss.y,i)
                    e_bullets1.append(eb)
                boss.e_shot1 = False    
            if player.bosstime1 +20 == time_elapsed:
                for i in range(36):
                    eb=Bossbullet1(boss.x,boss.y,i)
                    e_bullets1.append(eb) 
            if player.bosstime1 +40 == time_elapsed:
                for i in range(36):
                    eb=Bossbullet1(boss.x,boss.y,i)
                    e_bullets1.append(eb)
            if player.bosstime1 +60 == time_elapsed:
                for i in range(36):
                    eb=Bossbullet1(boss.x,boss.y,i)
                    e_bullets1.append(eb)
            if player.bosstime1 +80 == time_elapsed:
                for i in range(36):
                    eb=Bossbullet1(boss.x,boss.y,i)
                    e_bullets1.append(eb)
            if player.bosstime1 +180 == time_elapsed:         
                boss.stop = False
            #ボス弾幕2    
            if boss.e_shot2 == True:
                boss.stop = True
                player.bosstime2 = time_elapsed
                eb=Bossbullet2(boss.x,boss.y,player.x,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x-30,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x+30,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x-60,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x+60,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                boss.e_shot2 = False                
            if player.bosstime2 +20 == time_elapsed:
                eb=Bossbullet2(boss.x,boss.y,player.x,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x-45,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x+45,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
            if player.bosstime2 +40 == time_elapsed:
                eb=Bossbullet2(boss.x,boss.y,player.x,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x-30,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x+30,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x-60,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x+60,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
            if player.bosstime2 +60 == time_elapsed:
                eb=Bossbullet2(boss.x,boss.y,player.x,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x-45,player.y,boss.x,boss.y)
                e_bullets1.append(eb)
                eb=Bossbullet2(boss.x,boss.y,player.x+45,player.y,boss.x,boss.y)
                e_bullets1.append(eb)    
            if player.bosstime2 +120 == time_elapsed:         
                boss.stop = False

            #ボス用弾幕3    
            if boss.e_shot3 == True:
                player.bosstime3 = time_elapsed
                boss.stop = True
                for i in range(20):
                    eb=Bossbullet3(boss.x,boss.y,i,boss.x,boss.y)
                    e_bullets1.append(eb)
                boss.e_shot3 = False
            if player.bosstime3 +40 == time_elapsed:
                for i in range(20):
                    eb=Bossbullet3(boss.x,boss.y,i,boss.x,boss.y)
                    e_bullets1.append(eb)
            if player.bosstime3 +80 == time_elapsed:
                for i in range(20):
                    eb=Bossbullet3(boss.x,boss.y,i,boss.x,boss.y)
                    e_bullets1.append(eb)
            if player.bosstime3 +120 == time_elapsed:
                for i in range(20):
                    eb=Bossbullet3(boss.x,boss.y,i,boss.x,boss.y)
                    e_bullets1.append(eb)
            if player.bosstime3 +160 == time_elapsed:
                for i in range(20):
                    eb=Bossbullet3(boss.x,boss.y,i,boss.x,boss.y)
                    e_bullets1.append(eb)                
            if player.bosstime3 +240 == time_elapsed:                           
                boss.stop = False                
            if boss.hiteffect == True:
                ef = Particle(boss.x,boss.y)  
                particles.append(ef)
                boss.hiteffect = False
            screen.blit(boss.image,(boss.x-18,boss.y-30))
            if boss.death == True:
                bosses.remove(boss)
                player.bosskill = True
                de=Deathparticle(boss.x,boss.y,3)
                deathparticles.append(de)
                t=Timer(120)
                timers.append(t)
                
        for e_bullet1 in e_bullets1:
            e_bullet1.update()
            if(e_bullet1.judge(player) == True) and (player.life_lost_time + 120 < time_elapsed):
                    player.life_lost_time = time_elapsed
                    player.life -= 1
                    de=Deathparticle(player.x,player.y,1)
                    deathparticles.append(de)
                    if player.life == 0:
                        endFlag = True
            if (e_bullet1.x < -1000 or e_bullet1.x > 1000) or (e_bullet1.y < -1000 or e_bullet1.y > 1000):
                e_bullets1.remove(e_bullet1)

        if player.killcount > 20 and player.boss == False:
            for enemy1 in enemy1s:
                de=Deathparticle(enemy1.x,enemy1.y,2)
                deathparticles.append(de)
            enemy1s = []
            for enemy2 in enemy2s:
                de=Deathparticle(enemy2.x,enemy2.y,3)
                deathparticles.append(de)
            enemy2s = []
            for enemy3 in enemy3s:
                de=Deathparticle(enemy3.x,enemy3.y,4)
                deathparticles.append(de) 
            enemy3s = []
            boss = BOSS(320,100)
            bosses.append(boss) 
            player.boss = True     
        
        #パーティクルを管理
        for particle in particles:
            particle.update()
            if particle.t > 30:
                particles.remove(particle)  

        #撃破時パーティクルを管理
        for deathparticle in deathparticles:
            deathparticle.update()
            if deathparticle.t > 50:
                deathparticles.remove(deathparticle)

        #タイマーを管理
        for timer in timers:
            timer.update()
            if timer.t == True:
                endFlag = True
                                       
        screen.blit(player.image,(player.x-22,player.y-33))
        pygame.draw.circle(screen, COLORS[0], [player.x, player.y], 4)
 
        for i in range(player.life - 1):
            screen.blit(heart_image,(i * 30,50))
        pygame.display.update()
    
    if player.life == 0:
        dead(time_elapsed,force_quit)
    if player.bosskill == True:
        clear(time_elapsed,force_quit)
    else:
        quit(time_elapsed,force_quit)

        
#ゲームクリア時
def clear(time_elapsed,force_quit):
    if force_quit == False:
        endFlag = False
        font1 = pygame.font.SysFont(None, 40)
        text1 = font1.render("CONGRATULATIONS", False, (0,0,0))        
        while endFlag == False:
            screen.fill((0,0,0))
            screen.blit(backimage3,(0,0))
            screen.blit(text1,(180,200))                     
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    endFlag = True
                elif event.type == pygame.KEYDOWN:
                    endFlag = True
                    quit(time_elapsed,force_quit) 

#ゲームオーバー時
def dead(time_elapsed,force_quit):
    if force_quit == False:
        endFlag = False
        font1 = pygame.font.SysFont(None, 40)
        text1 = font1.render("GAME OVER...", False, (255,255,255))        
        while endFlag == False:
            screen.fill((0,0,0))
            screen.blit(backimage1,(0,0))
            screen.blit(text1,(210,200))                      
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    endFlag = True
                elif event.type == pygame.KEYDOWN:
                    endFlag = True
                    quit(time_elapsed,force_quit)


def quit(time,force_quit):
    if force_quit == False:
        endFlag = False
        t = time/59
        font1 = pygame.font.SysFont(None, 40)
        text1 = font1.render("your time: " + '{:.3f}'.format(t), False, (255,255,255))
        text2 = font1.render("Press Any Key to Re-Start", False, (255,255,255))

        while endFlag == False:
            screen.fill((0,0,0))
            screen.blit(backimage1,(0,0))
            screen.blit(text1,(210,200))
            screen.blit(text2,(150,240))
            screen.blit(player_image,(40,80))    
            screen.blit(enemy1_image,(140,80)) 
            screen.blit(enemy2_image,(240,80)) 
            screen.blit(player_image,(340,80))    
            screen.blit(enemy1_image,(440,80)) 
            screen.blit(enemy2_image,(540,80)) 

            screen.blit(player_image,(140,400))    
            screen.blit(enemy1_image,(240,400)) 
            screen.blit(enemy2_image,(340,400)) 
            screen.blit(player_image,(440,400))    
            screen.blit(enemy1_image,(540,400)) 
            screen.blit(enemy2_image,(40,400))  

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    endFlag = True
                elif event.type == pygame.KEYDOWN:
                    endFlag = True
                    main()

if __name__ == "__main__":
    open()
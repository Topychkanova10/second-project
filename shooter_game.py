#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
mixer.init()

mixer.music.load('space.ogg')#создаем фоновую музыку
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('fire.ogg')#создаем звук выстрела
fire_sound.set_volume(0.2)    
mixer.music.play()#проигрывать фоновую музыку


win_width = 700
win_hight = 500

FPS = 45
timer = time.Clock()

window = display.set_mode((win_width,win_hight))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'), (win_width,win_hight))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))#отобразить фон картинку в окне

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()#список состояния всех клавиш клавиатуры

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()        
#if bullet 
#bullet.remove(bullets)

rocket = Player('rocket.png', 5, win_hight - 120, 80, 120, 5)


monsters = sprite.Group()#создаём группу спрайтов
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,2))
    monsters.add(monster)
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1,2))
    asteroids.add(asteroid)

lost = 0
score = 0
life = 3

font1 = font.SysFont('Arial', 36)#font - 
font2 = font.SysFont('Arial', 72)
#font3 = font.Font(None, 54)#шрифт для жизней

game = True
finish = False
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                fire_sound.play()
                
    if not finish:
        window.blit(background, (0,0))

        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        rocket.reset()#обновляем движение спрайтов в новом местоположении
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)#при столкновении удалить монстров и пули
        for goblin in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,2))
            monsters.add(monster)
        
        #if sprite.spritecollide(rocket, asteroids, False) or sprite.spritecollide(rocket, monsters, False):
            #sprites.spritecollide(rocket, asteroid, True)
            #sprites.spritecollide(rocket, monsters, True)
            #life -= 1

        #условие выйгрыша
        if score >= 10:
            finish = True
            win = font2.render('YOU WIN!', True, (0, 255, 13)) 
            window.blit(win, (200, 200))
            mixer.music.pause()
            fire_sound.stop()
        
        #условие проигрыша
        if lost >= 5 or life == 0 or sprite.spritecollide(rocket, asteroids, False) or sprite.spritecollide(rocket, monsters, False):
            finish = True            
            lose = font2.render('YOU LOSE!', True, (255, 0, 0)) 
            window.blit(lose, (200, 200))
            mixer.music.pause()
            fire_sound.stop()

        text_lose = font1.render('Пропущено: ' + str(lost), True, (255,255,255))
        window.blit(text_lose, (10, 45))

        text_win = font1.render('Счет: ' + str(score), True, (255,255,255)) 
        window.blit(text_win, (10, 10))

        #life_counter = font3.render(str(life), True, (127, 255, 0))#life counter - счетчик жизней
        #window.blit(life_counter, (650,10))

        display.update()        
    timer.tick(FPS)   
     
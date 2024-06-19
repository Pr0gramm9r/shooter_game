


#hello

import pygame as pg

from random import randint

class Base_sprite(pg.sprite.Sprite):
    def __init__(self, pic, x, y, w, h, hb_x = 0, hb_y = 0):
        super().__init__()
        self.picture = pg.transform.scale(pg.image.load(pic), (w, h))
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = self.picture
        
        center = self.rect.center
        self.rect.width = self.rect.width - self.rect.width/100*hb_x
        self.rect.height = self.rect.height - self.rect.height/100*hb_y
        self.rect.center = center
        self.delta_x = self.rect.x - x
        self.delta_y = self.rect.y - y

    def draw(self):
        mw.blit(self.picture, (self.rect.x, self.rect.y))
        #pg.draw.rect(mw, (255, 0, 0), self.rect, 3)

class Hero(Base_sprite):
    speed = 6
    energy = 0
    health = 100
    points = 0
    life = 3
    missed = 0 

    def update(self):
        self.energy += 1
        keys = pg.key.get_pressed()

        if (keys[pg.K_LEFT] or keys [pg.K_a]) and self.rect.x >= 5:
            self.rect.x -= self.speed

        if (keys[pg.K_RIGHT] or keys [pg.K_d]) and self.rect.x <= win_w - self.rect.width:
            self.rect.x += self.speed
    
        if (keys[pg.K_UP] or keys [pg.K_w]) and self.rect.y >= 5:
            self.rect.y -= self.speed

        if (keys[pg.K_DOWN] or keys [pg.K_s]) and self.rect.y <= win_h - (self.rect.width + 20):
            self.rect.y += self.speed
    
        if keys[pg.K_SPACE]:
            self.fire()
    
    def fire(self):
        fire.play()
        if self.energy > 20:
            self.energy = 0
            bullet = Bullet('bullet2.png', self.rect.x + 25, self.rect.y, 20, 40)
            bullets.add(bullet)

    def draw(self):
        super().draw()
        rect = pg.Rect(self.rect.x, self.rect.bottom + 5, self.rect.width/100 * self.health, 7)   
        
        g = int(255/100*self.health)

        if g < 0:
            g = 0

        r = int(255 - g)

        b = 70

        pg.draw.rect(mw, (r, g, b), rect) 

    
                 


class Star(Base_sprite): 
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_h:
            stars.remove(self)

class Ufo(Base_sprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_h:
            ufos.remove(self)
            hero.missed += 1

class Bullet(Base_sprite):
    speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            bullets.remove(self)

class Boom(pg.sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1

        if self.frame_num > len(self.frames) - 1:
            self.frame_num = 0
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()

class Meteor(Boom):

    def __init__(self, center, meteor_sprites, meteors) -> None:
        super().__init__(center, meteor_sprites, meteors)
        self.speed_x = randint(1, 8)
        self.speed_y = randint(-8, 8)

    def update(self):
        self.next_frame()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    
def make_star():
    size = randint(15, 30)
    star = Star('star.png', randint(0,win_w), 10, size, size)
    star.speed = randint(1, 10)
    stars.add(star)

def make_ufo(pic):
    size1 = randint(80, 90)
    size2 = randint(60, 70)
    ufo = Ufo(pic, randint(0,win_w), -100, size1, size2)
    ufo.speed = randint(1, 2)
    ufos.add(ufo)

def ufo_collide():
    for bullet in bullets:
        for ufo in ufos:
            if bullet.rect.colliderect(ufo.rect):
                    bullets.remove(bullet)
                    ufos.remove(ufo)
                    hero.points += 1

def set_text(text, x, y, color = (255, 255, 200)):
    mw.blit(font.render(text, True, color), (x,y))

def sprites_load(folder, file_name, size, colorkey = (0,0,0)):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = pg.image.load(f'{folder}\\{file_name}{num}.png')
            spr = pg.transform.scale(spr,size)
            if colorkey: spr.set_colorkey(colorkey)
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites

pg.font.init()

font = pg.font.Font(None, 36)

win_w = 700
win_h = 500

boom_sprites = sprites_load('boom4', 'boom', (80,80))

meteor_sprites = [
    sprites_load('meteor1', 'meteor', (20,20)),
    sprites_load('meteor1', 'meteor', (30,30)),
    sprites_load('meteor1', 'meteor', (40,40)),
    sprites_load('meteor1', 'meteor', (60,60)),
    sprites_load('meteor1', 'meteor', (70,70)),
    sprites_load('meteor1', 'meteor', (50,60))
]

mw = pg.display.set_mode((win_w, win_h)) 
pg.display.set_caption('SHOOTER')
clock = pg.time.Clock()

pg.mixer.init()
pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
fire = pg.mixer.Sound('fire1.ogg')
boom_sound = pg.mixer.Sound('boom1.ogg')



fon = pg.transform.scale(pg.image.load('fon.png'), (win_w, win_h))
fon_end1 = pg.transform.scale(pg.image.load('game over.png'), (win_w, win_h))

hero = Hero('rocket2.png', win_w/2 - 35, win_h - 150, 100, 90)

stars = pg.sprite.Group()
booms = pg.sprite.Group()
ufos = pg.sprite.Group()
bullets = pg.sprite.Group()
meteors = pg.sprite.Group()


mw.blit(fon, (0, 0))

ticks = 0
win = False
play = True
game = True
while play:

    for e in pg.event.get():
        if e.type == pg.QUIT or \
                (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
            play = False 

    if game:
        mw.blit(fon, (0,0))

        if ticks % 15 == 0:
            make_star()

        if ticks % 50 == 0:
            Meteor((randint(0, win_w), -100), meteor_sprites[randint(0, len(meteor_sprites) - 1)], meteors)
            

        
        while len(ufos) < 6:
            make_ufo('ufo.png')
            make_ufo('ufo1.png')
            
        stars.update()
        ufos.update()
        bullets.update()
        booms.update()
        hero.update()
        meteors.update()

        #коллизии пулей и НЛО

        collides = pg.sprite.groupcollide(bullets, ufos, True, True)
        
        for ufo, bullet in collides.items():
            Boom(ufo.rect.center, boom_sprites, booms)
            hero.points += 1
            boom_sound.play()

        #коллизии корабля и НЛО

        if pg.sprite.spritecollide(hero, ufos, False):
            hero.health -= 1

            if hero.health <= 0:
                game = False

        stars.draw(mw)
        ufos.draw(mw)
        bullets.draw(mw)
        booms.draw(mw)
        hero.draw()
        meteors.draw(mw)


        set_text(f'Очки: {hero.points}', 50, 20)
        set_text(f'Жизни: {hero.life}', win_w - 150, 20)
        set_text(f'Пропущенные: {hero.missed}', 200, 20)


    else:
        mw.blit(fon_end1, (0,0))
        play = False
        
    pg.display.update()
    clock.tick(60)
    ticks += 1

import pygame
from constants import *
import math
from spritesheetHandler import *

pygame.init()

tanks_c = pygame.sprite.Group()
bullets_c = pygame.sprite.Group()
barrers_c = pygame.sprite.Group()

class Tank(pygame.sprite.Sprite):
  
  correction_angle = 90
  
  def __init__(self, tankcolor, x, y, player):
    super().__init__()
    self.player = player
    self.color = tankcolor
    tanksprite = spritelist["tank"+tankcolor+"_outline"]
    self.image = tanksprite
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0, 0)
    self.vel.x = self.vel[0]
    self.vel.y = self.vel[1]
    self.velc = tankvelc
    self.target = None
    self.dead = False
    self.bulletvel = bulletvelc
    tanks_c.add(self)
    tanks.append(self)

  def render(self, surface):
    collisions = pygame.sprite.spritecollideany(self, barrers_c)
    surface.blit(self.image, (self.x * SCALEX - self.image.get_width()//2, self.y * SCALEY - self.image.get_height()//2))

  def move(self, keys_pressed): 
    
    if self.player and not self.dead:
      if keys_pressed==pygame.K_a:
        self.vel.x = -self.velc
      elif keys_pressed==pygame.K_d:
        self.vel.x = self.velc
      else:
        self.vel.x = 0

      if keys_pressed==pygame.K_w:
        self.vel.y = -self.velc
      elif keys_pressed==pygame.K_s:
        self.vel.y = self.velc
      else:
        self.vel.y = 0
        
  def update(self,screen):

    self.x += self.vel.x
    self.y += self.vel.y
    mx, my = pygame.mouse.get_pos()
    angle = math.degrees(math.atan2(( self.y- my), (mx - self.x))) - self.correction_angle
    rot_image = pygame.transform.rotate(self.image, angle)
    self.image = rot_image

    self.rect.x = self.x * SCALEX - self.image.get_width()//2
    self.rect.y = self.y * SCALEY - self.image.get_height()//2

  def set_target(self, target):
    self.target = target

  def get_path_to_target(self): 
    # uses bresenham's line drawing algorithm
    if self.target is None:
      return None

    start = (self.rect.centerx, self.rect.centery)
    end = (self.target.rect.centerx, self.target.rect.centery)
    path = [(start[0], start[1])]
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x = x1
    y = y1
    n = 1 + dx + dy
    x_inc = 1 if x2 > x1 else -1
    y_inc = 1 if y2 > y1 else -1
    error = dx - dy
    dx *= 2
    dy *= 2

    for i in range(n):
      path.append((x, y))
      if error > 0:
        x += x_inc
        error -= dy
      else:
        y += y_inc
        error += dx

    return path

  def has_line_of_sight(self, target):
    if target is None:
      return False
      
    for barrier in barrers_c:
      if pygame.sprite.collide_rect(self, barrier):
        return False

    return True

  def fire_at_target(self):
    if self.target is None:
      return

    if self.has_line_of_sight(self.target):
      mx, my = self.target.rect.center
      angle = math.degrees((math.atan2( self.y- my), (mx - self.x)) - self.correction_angle)
      bullet = Bullet(self.bulletsprite, self.rect.centerx, self.rect.centery, self.bulletvel, bounceLimit)
      bullet.image = pygame.transform.rotate(bullet.image, angle)
      bullets_c.add(bullet)
    
    
  def shoot(self):  
    bullet = Bullet(spritelist["bullet"+self.color], self.x, self.y, self.bulletvel)
    bullets_c.add(bullet)
    bullets.append(bullet)
    
  def kill(self):
    self.vel = (0,0)
    tanks_c.remove(self)
    tanks.remove(self)
    self.dead= True
        
  def beta_peaceful(self):
    corners = [(0, 0), (0, VIEW_HEIGHT), (VIEW_WIDTH, 0), (VIEW_WIDTH, VIEW_HEIGHT)]
    distlist = []
    for i in range(len(corners)):
      distlist.append(math.sqrt((corners[i][0] - self.x)**2 + (corners[i][1] - self.y)**2))
    cc = distlist.index(min(distlist)) #closest corner 
    angle = math.atan2(corners[cc][1]-self.y, corners[cc][0]-self.x)
    self.vel = pygame.math.Vector2(math.cos(angle) * self.velc, math.sin(angle) * self.velc)  
        
        
      

class Bullet(pygame.sprite.Sprite):
  correction_angle = 90
      
  def __init__(self, bulletsprite, x, y, bulletvel):
    super().__init__()
    mx, my = pygame.mouse.get_pos()
    angle = math.degrees(math.atan2(( y- my), (mx - x))) - self.correction_angle
    self.image = pygame.transform.rotate(bulletsprite, angle)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0, -bulletvel)
    self.bounce_limit = bounceLimit
        
  def destroy(self):
    bullets_c.remove(self)
    bullets.remove(self)
    
  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))

  def update(self, screen):
    
    self.check_collision()
    self.rect.x += self.vel.x
    self.rect.y += self.vel.y

    if self.rect.bottom < 0:
      self.kill()      
      
  def bounce(self, collisions):
    self.bounces += 1
    if self.bounces > self.bounce_limit:
      self.kill()
    else:
      #sound 
      self.vel.reflect_ip(collisions[0].normal)
      angle = math.degrees(math.atan2(-self.vel.y, self.vel.x))
      self.image = pygame.transform.rotate(self.image, angle)
      
  def check_collision(self):
    collisions = pygame.sprite.groupcollide(bullets_c, barrers_c, False, False, pygame.sprite.collide_mask)
    if len(collisions)>0:
      for bullet in collisions.keys():
        bullet.bounce(collisions.values)

class Barrier(pygame.sprite.Sprite):
  def __init__(self, spritename):
    super().__init__()
    self.image = spritelist[spritename]
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    barrers_c.add(self)
    
    

import pygame
from constants import *
import math

pygame.init()

shooters = pygame.sprite.Group()
bullets = pygame.sprite.Group()
barriers = pygame.sprite.Group()

class Tank(pygame.sprite.Sprite):
  
  dead = False
  correction_angle = 90
  
  def __init__(self, tankSprite, x, y, w, h):
    super().__init__()
    self.image = pygame.transform.scale(tankSprite, (w, h))
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0, 0)
    self.velc = tankvelc

  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))

  def update(self, screen):
    keys_pressed = pygame.key.get_pressed()
    
    if not self.dead:
      if keys_pressed[pygame.K_a]:
        self.vel.x = -self.velc
      elif keys_pressed[pygame.K_d]:
        self.vel.x = self.velc
      else:
        self.vel.x = 0

      if keys_pressed[pygame.K_w]:
        self.vel.y = -self.velc
      elif keys_pressed[pygame.K_s]:
        self.vel.y = self.velc
      else:
        self.vel.y = 0

      self.x += self.vel.x
      self.y += self.vel.y
      self.collisionMask(screen)
      mx, my = pygame.mouse.get_pos()
      angle = math.degrees((math.atan2( self.y- my), (mx - self.x)) - self.correction_angle)
      rot_image = pygame.transform.rotate(self.image, angle)
      self.image = rot_image
    

  def shoot(self):  
    bullet = Bullet(self.bulletSprite, self.rect.centerx, self.rect.centery, self.bulletvel)
    bullets.add(bullet)
    
  def kill(self):
    shooters.remove(self)
    self.dead= True

class Bullet(pygame.sprite.Sprite):
  correction_angle = 90
  
  def __init__(self, bulletSprite, x, y, bulletvel, bounceLimit):
    super().__init__()
    mx, my = pygame.mouse.get_pos()
    angle = math.degrees((math.atan2( self.y- my), (mx - self.x)) - self.correction_angle)
    self.image = pygame.transform.rotate(bulletSprite, angle)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0, -bulletvel)
    self.bounce_limit = bounceLimit
    
  def destroy(self):
    bullets.remove(self)
    
  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))

  def update(self, screen):
    
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
      
  def check_collision(self,shooters,barriers):
    collisions = pygame.sprite.groupcollide(shooters, barriers, False, False, pygame.sprite.collide_mask)
    if len(collisions)>0:
      for bullet in collisions.keys():
        bullet.bounce(collisions.values)

class Terrain(pygame.sprite.Sprite):
  #IMP: NEEDS REAL SCREEN ATTRIBUTES
  def __init__(self, ground, surface):
    super().__init__()
    self.image = pygame.transform.scale (ground, (surface.get_width(), surface.get_height()))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    barriers.add(self)

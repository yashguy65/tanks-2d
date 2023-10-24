import pygame , random
from constants import *
from spritesheetHandler import SpriteSheet

pygame.init()

shooters = pygame.sprite.Group()
barriers = pygame.sprite.Group()

class Tank(pygame.sprite.Sprite):
  def __init__(self, tankSprite, x, y, w, h, tankvelc):
    super().__init__()
    self.image = pygame.transform.scale(tankSprite, (w, h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0, 0)
    self.velc = tankvelc

  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))

  def update(self, screen, keys_pressed):
    if keys_pressed[pygame.K_LEFT]:
      self.vel.x = -self.velc
    elif keys_pressed[pygame.K_RIGHT]:
      self.vel.x = self.velc
    else:
      self.vel.x = 0

    if keys_pressed[pygame.K_UP]:
      self.vel.y = -self.velc
    elif keys_pressed[pygame.K_DOWN]:
      self.vel.y = self.velc
    else:
      self.vel.y = 0

    self.rect.x += self.vel.x
    self.rect.y += self.vel.y

  def shoot(self):  
    bullet = Bullet(self.bulletSprite, self.rect.centerx, self.rect.centery, self.bulletvel)
    shooters.add(bullet)

class Bullet(pygame.sprite.Sprite):
  def __init__(self, bulletSprite, x, y, bulletvel, bounceLimit):
    super().__init__()
    self.image = bulletSprite
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0, -bulletvel)
    self.bounce_limit = bounceLimit
    
  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))
    
  def kill(self):
    shooters.remove(self)

  def update(self, screen):
    self.rect.x += self.vel.x
    self.rect.y += self.vel.y

    if self.rect.bottom < 0:
      self.kill()
      
  def bounce(self):
    self.bounces += 1
    if self.bounces > self.bounce_limit:
      self.kill()
    else:
      #sound 
      
      pass
      
  def check_collision():
    collisions = pygame.sprite.groupcollide(shooters, barriers, True, False, pygame.sprite.collide_mask)
    for bullet, in collisions.keys():
      bullet.bounce(collisions.values)
        
      

'''class EnemyTanks(pygame.sprite.Sprite):

  def __init__(self,cloudSprite, x, y, w, h,cloudvelc):
    super().__init__()
    self.image = pygame.transform.scale(cloudSprite, (w, h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(0,0)
    self.vel.x=(random.random())*cloudvelc

  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))
  def update(self, screen, playerclass):
    playervelx = playerclass.vel.x
    self.rect.x += self.vel.x
    shooters.add(self)

  def cloudspawn(camera, cameradist, Terrainclass, sprite,safedist,maxcloudlimit):
    safespawn = True
    x=random.random()*SCREEN_WIDTH
    y=SCREEN_HEIGHT/2 * random.random()
    # if <=0 or abs(player.y-y)<safedist:
    if camera.rect.left-cameradist<=x<=camera.rect.right+cameradist or camera.rect.top-cameradist<=y<=camera.rect.bottom+cameradist or len(cloudlist)>(maxcloudlimit-1):
      safespawn=False
    
    for cloud in cloudlist:
      if abs(cloud.rect.x-x)<=safedist and abs(cloud.rect.y-y)<=safedist :
        safespawn=False
        break
    if safespawn==True:
      #print("cloud:",x,y,)
      cloudvar=Cloud(cloudSprite=sprite, x=x, y=y, **CLOUD_ARGS)
      collidedmask = pygame.sprite.collide_mask(cloudvar, Terrainclass)
      if collidedmask == None:
        cloudlist.append(cloudvar)
    # else:
      # print("cloud not allowed")
  def cloudupdate(surf, player):
    for cloudvar in cloudlist:
      cloudvar.update(surf,player)
      cloudvar.render(surf)
      if cloudvar.rect.x > SCREEN_WIDTH or cloudvar.rect.y > SCREEN_HEIGHT or cloudvar.rect.y < 0 or cloudvar.rect.x < 0:
        #kill()
        cloudlist.remove(cloudvar)
        # print('Removed cloud')
    # print(len(cloudlist),"clouds")
    
class Bird(pygame.sprite.Sprite):

  def __init__(self, birdSprite, x, y, w, h, birdvelx, birdvely):
    super().__init__()
    self.image = pygame.transform.scale(birdSprite, (w, h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.mask = pygame.mask.from_surface(self.image)
    self.vel = pygame.math.Vector2(2,2)

  def update(self, screen):
    birdvelx = 4
    birdvely = 2
    self.rect.x += self.vel.x
    self.rect.y += self.vel.y

    if self.rect.y < 50:
      self.vel = pygame.math.Vector2(birdvelx, birdvely)

    if 0<=self.rect.y <= SCREEN_HEIGHT/2 and self.vel.y<0:
      self.vel = pygame.math.Vector2(birdvelx, -birdvely)

    if 0<=self.rect.y <= SCREEN_HEIGHT/2 and self.vel.y>0:
      self.vel = pygame.math.Vector2(birdvelx, birdvely)

    if self.rect.y >= SCREEN_HEIGHT/2:
      self.vel = pygame.math.Vector2(birdvelx, -birdvely)

    #if self.rect.x >= (SCREEN_WIDTH - self.rect.w) or self.rect.x <= 0:
     # self.rect.x = 100
      #self.rect.y = 100

    shooters.add(self)

  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))

  def birdspawn(camera, cameradist, Terrainclass, sprite, safedist, maxbirdlimit):

    safespawn = True
    x=random.random()*SCREEN_WIDTH
    y=SCREEN_HEIGHT/2 * random.random()
    if camera.rect.left-cameradist<=x<=camera.rect.right+cameradist or camera.rect.top-cameradist<=y<=camera.rect.bottom+cameradist or len(birdlist)>(maxbirdlimit-1):
      safespawn=False
    for bird in birdlist:
      if abs(bird.rect.x-x)<=safedist  and abs(bird.rect.y-y)<=safedist :
        safespawn=False
        break
    if safespawn==True:
      # print("bird:",x,y)
      birdvar=Bird(birdSprite=sprite, x=x, y=y, **BIRD_ARGS)
      collidedmask = pygame.sprite.collide_mask(birdvar, Terrainclass)
      if collidedmask == None:
        birdlist.append(birdvar)

  def birdupdate(surf):
    for birdvar in birdlist:
      birdvar.update(surf)
      birdvar.render(surf)
      if birdvar.rect.x > SCREEN_WIDTH or birdvar.rect.y > SCREEN_HEIGHT or birdvar.rect.y < 0 or birdvar.rect.x < 0:
        #kill()
        birdlist.remove(birdvar)
    # print(len(birdlist),"birds")'''

class Terrain(pygame.sprite.Sprite):
  #IMP: NEEDS REAL SCREEN ATTRIBUTES
  def __init__(self, ground, surface):
    super().__init__()
    self.image = pygame.transform.scale (ground, (surface.get_width(), surface.get_height()))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    barriers.add(self)

class Sprite(pygame.sprite.Sprite):

  def __init__(self,imageSprite, x, y, w, h, rot_angle_constant, max_thrust_mag):
    super().__init__()
    self.x = x
    self.y = y
    self.image = pygame.transform.scale(imageSprite, (w,h))
    self.mask = pygame.mask.from_surface(self.image) # used if rough detection passes
    self.rect = pygame.Rect(0,0,w,h) #for rough collision detection
    self.rect.center = (self.x,self.y)
    self.origin = (self.rect.x, self.rect.y) #point at which to draw the image
    self.vel = pygame.math.Vector2(0,0)
    self.thrust = Thrust(0, 0)
    self.max_thrust_mag=max_thrust_mag

    self.thrustc = 0.01

    self.rot_angle = 0# angle by which to rotate per frame
    self.rot_angle_constant=rot_angle_constant
    self.angle = 0 # angle wrt x axis, counterclockwise
    self.RESTART_NEEDED = False
    self.MASK_NEEDED = False
    # Permanent copies of initial properties; do not modify

    self.IMAGE = self.image
    self.RECT = self.rect
    self.ANGLE = self.angle
  def rot_center(self, n): #n is either 1 or -1; for direction of rotation

    rot = n*self.rot_angle
    self.angle = (self.angle + rot) % 360

    rot_image = pygame.transform.rotate(self.IMAGE, self.angle)
    self.mask = pygame.mask.from_surface(rot_image, 0)
    rot_rect = rot_image.get_rect()

    rot_rect.center = self.rect.center

    self.rect = rot_rect
    self.image = rot_image

  def collisionMask (self, screen):

    plane_collided = pygame.sprite.spritecollide(self, shooters, False, pygame.sprite.collide_mask)
    #print(plane_collided)
    #collidedmask = pygame.sprite.collide_mask(self, Cloud)
    if plane_collided != []:
      self.RESTART_NEEDED = True

  def collisionWindow(self, screen):

    if self.rect.x >= (SCREEN_WIDTH - self.rect.w) or self.rect.x <= 0:#self.rect.w:
      self.rect.x = SCREEN_WIDTH - self.rect.w
      self.RESTART_NEEDED = True

    elif self.rect.y >= (SCREEN_HEIGHT - self.rect.h) or self.rect.y <= 0:#self.rect.h:
      self.rect.y = SCREEN_HEIGHT - self.rect.h
      self.RESTART_NEEDED = True

    elif self.rect.x <= 0:
      self.rect.x = 0

    elif self.rect.y <= 0:
      self.rect.y = 0


  def update(self, keys, KEYMAP, screen, toRun,maxvel):

    if toRun:
      self.vel += self.thrust.get_vec()

      self.x += self.vel.x
      self.y += self.vel.y

      # print(self.vel.magnitude())

      self.rect.center = (self.x, self.y)

      if keys[KEYMAP['tiltup']]:
        self.thrust.dir = self.thrust.dir.rotate(-self.rot_angle)
        self.rot_center(1)

      if keys[KEYMAP['tiltdown']]:
        self.thrust.dir = self.thrust.dir.rotate(self.rot_angle)
        self.rot_center(-1)

      if keys[KEYMAP['accel']]:
        if self.thrust.magnitude+self.thrustc<self.max_thrust_mag:
          self.thrust.magnitude += self.thrustc
      ## In case we need to make it only accel as long as key is pressed
        else:
          self.thrust.magnitude=self.max_thrust_mag

      if keys[KEYMAP['decel']]:
        if self.thrust.magnitude-self.thrustc >= 0:
          self.thrust.magnitude -= self.thrustc
        else:
          self.thrust.magnitude = 0
      self.collisionMask(screen)
      self.rot_angle=(self.rot_angle_constant)*(self.vel.magnitude()**0.90)
  def render(self, surface):
    surface.blit(self.image, (self.rect.x, self.rect.y))
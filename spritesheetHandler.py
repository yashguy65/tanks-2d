import pygame
from bs4 import BeautifulSoup
from constants import COLORKEY

class SpriteSheet:

    def __init__(self, filename): 
        
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey = COLORKEY):
        
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
        
    def loadXML(self):
        
        names,xs,ys,widths,heights = [],[],[],[],[]
        
        with open('sheet_tanks.xml') as f:
            data = f.read()
            parsed_data = map (str, (BeautifulSoup(data, "xml")).find_all("SubTexture"))
            
            #<SubTexture height="78" name="tankBlack_outline.png" width="83" x="568" y="362"/>
            
            a =  'height="'
            b =  '" name="' 
            c =  '.png" width="'
            d =  '" x="'
            e =  '" y="'
            f =  '"/>'
            
            for i in parsed_data:
                
                ia = i.find(a) + 8
                ib = i.find(b) + 8
                ic = i.find(c) + 13
                id = i.find(d) + 5
                ie = i.find(e) + 5
                iF = i.find(f)
                
                heights.append(i[ia:ib-8])
                names.append(i[ib:ic-13])
                widths.append(i[ic:id-5])
                xs.append(i[id:ie-5])
                ys.append(i[ie:iF])
                
        spritelist = {}
        
        for i in range(len(names)):
            spritelist[(names[i]).lower()] = self.image_at((int(xs[i]), int(ys[i]), int(widths[i]), int(heights[i])))
            
        return spritelist
    
ss = SpriteSheet("sheet_tanks.png")
spritelist = ss.loadXML()

            
    
            
                
            
            
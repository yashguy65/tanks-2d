import pygame
from bs4 import BeautifulSoup

class SpriteSheet:

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey = None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    def readXML(self):
        with open('sheet_tanks.xml') as f:
            data = f.read()
            parsed_data = BeautifulSoup(data, "xml")
            names_parsed = parsed_data.find_all("name")
            xs_parsed = parsed_data.find_all("x")
            ys_parsed = parsed_data.find_all("y")
            widths_parsed = parsed_data.find_all("width")
            heights_parsed = parsed_data.find_all("height")
            names = [i for i in names_parsed]
            xs = [i for i in xs_parsed]
            ys = [i for i in ys_parsed]
            widths = [i for i in widths_parsed]
            heights = [i for i in heights_parsed]
            return names,xs,ys,widths,heights
        
    def loadXML(self,names,xs,ys,widths,heights):
        p = {}
        for i in range(len(names)):
            p[(names[i].text)] = self.image_at((int(xs[i].text), int(ys[i].text), int(widths[i].text), int(heights[i].text)))
        return p
            
    
            
                
            
            
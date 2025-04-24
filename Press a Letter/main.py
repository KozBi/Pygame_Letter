import pygame
from sys import exit
import string
import random

#inherit form pygame.class.Sprite
class Letter(pygame.sprite.Sprite):

    def __init__(self,x, y=0):
        super().__init__()
        self._random_letter = random.choice(tuple(string.ascii_lowercase))
        self.font= pygame.font.Font("fonts/LEMONMILK-LightItalic.otf", 30)
        self.color = "black"
        self.y=y

        self._surface = self.font.render(self._random_letter, True,self.color)
        self.rect = self._surface.get_rect(topleft=(x,y))
    
    def draw(self, screen):
        screen.blit(self._surface, self.rect)
    
    def update_and_move (self,dy,dx=0):
        #move_ip - it moves the same rectangle, it doesn't generate a new one
        self.rect.move_ip(dx,dy)

        if self.rect.bottom > 530:
            self._surface = self.font.render(self._random_letter, True,"RED")

class Button:



    def __init__(self, text, pos, font, padding=(20, 10), 
                 text_color=(255,255,255), color=("#1E2234"), 
                 hover_color=("#5A669C"), border_color=(255,255,255), 
                 border_radius=20):

        self.text = text
        self.font = font
        self.padding = padding
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.clicked = False

        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()

        width = self.text_rect.width + 2 * self.padding[0]
        height = self.text_rect.height + 2 * self.padding[1]
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        current_color = self.color
        current_rect = self.rect.copy()
        radius = self.border_radius

        # Hover 
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        # Draw button 
        pygame.draw.rect(screen, current_color, current_rect, border_radius=radius)

        # Draw text centered
        self.text_rect.center = current_rect.center
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos):
            if mouse_click[0]:  # Left mouse button
                return True
            else:
                if self.clicked:
                    return False  # reset click after release

class Game:
    def __init__(self,width=900,height=600):

        pygame.init()
        pygame.display.set_caption("Press a Letter:")

        self.width=width
        self.height=height

        #config
        self.max_let_on_screen=50
        self.columns= [clmn * 30 for clmn in range(30)] #column * 30  column=(0...29) -> 0, 30 ,60, 90 #split screen for collumns -> 30 columns 900/30
        self.FPS = 60

        self.clock =pygame.time.Clock()

        #init value
        self.score = 0
        self.lifes= 3
        self._start_time = 0
        self.last_difficult = 0  
        self._game_mode='START' # can be also # 'PLAY' and 'END'
        self.difficult =1

        self._start_time=(pygame.time.get_ticks())
        self._letters_group= pygame.sprite.Group() #Group of letters in special pygame containter class Group

        #main screen
        self.main_screen = pygame.display.set_mode((self.width,self.height))
        self.grph_background = pygame.image.load("graphics/Background.jpg").convert_alpha() #convert jpg for python to run faster (alpha fill backgrand of the image or smth.)  
        self.screen_rect = self.main_screen.get_rect() 
        self.main_screen_centrum = self.screen_rect.center 


        #used Fonts
        self.Font1 = pygame.font.Font("fonts/LEMONMILK-LightItalic.otf", 20)

        # define buttons 
        self.buttons = {"start" : Button("Start Game", pos=self.main_screen_centrum , font=self.Font1),
                  "again" : Button("Try again", pos=(self.main_screen_centrum[0]-100,self.main_screen_centrum[1]), font=self.Font1),
                  "close" : Button("Close Game", pos=(self.main_screen_centrum[0]+100,self.main_screen_centrum[1]) , font=self.Font1)}   
           
        #timers
        self.letter_timer = pygame.USEREVENT + 1

    def _genere_letter(self):
            if len(self._letters_group)<=self.max_let_on_screen:
                pos_x=random.choice(self.columns)
                column_occupied=False
                if len(self._letters_group)>0:
                    for L in self._letters_group:
                        if L.rect.x == pos_x:
                            column_occupied=True
                            break
                    if not column_occupied:
                        self._letters_group.add(Letter(pos_x))
                else:       
                    self._letters_group.add(Letter(pos_x))
    
    def _init_game(self):
        self.score = 0
        self.lifes= 3
        self._start_time = 0
        self._letters_group.empty()
        self._game_mode='PLAY'

    def _start_screen(self):
        #Game Star screen        
        self.buttons['start'].draw(self.main_screen)
        if self.buttons['start'].is_clicked():
            self._game_mode='PLAY'
            self.start_time= pygame.time.get_ticks()
            self._init_game()

    def _game_start(self):

        current_time = (pygame.time.get_ticks()) - self.start_time
        if current_time < 5000:
            self.difficult = 1
        elif current_time < 10000:
            self.difficult = 2
        elif current_time < 20000:
            self.difficult = 3

        if self.difficult != self.last_difficult: #logik to triger this only once for performance reasons.
            pygame.time.set_timer(self.letter_timer, int(1000 / self.difficult))
            self.last_difficult = self.difficult

        txt_score = self.Font1.render((f"Your score: {self.score}"), True,"black")
        txt_lives = self.Font1.render((f"Lifes: {self.lifes}"), True,"black")


        self.main_screen.blit(txt_score,(10,550))
        self.main_screen.blit(txt_lives,(800,550))
        pygame.draw.lines(self.main_screen, "black",True,[(0, 525),(900, 525)],3)

        keys = pygame.key.get_pressed()
        if self._letters_group :
            for char in self._letters_group:    
                char.draw(self.main_screen)
                char.update_and_move(2)
                if keys[pygame.key.key_code(F'{char._random_letter}')] and self.pressed_key_letter:
                    char.kill()
                    self.score+=1
                    break
                elif char.rect.y > 530: 
                        char.kill()
                        self.lifes-=1
        #lose condition
        if self.lifes <=0: 
            self._game_mode='END'

    def _game_end(self):
        self.main_screen.blit(self.grph_background,(0,0))
        txt_score1 = self.Font1.render(("Your games has ended"), True,"black")
        txt_score2 = self.Font1.render((f"Your score: {self.score}"), True,"black")
        self.main_screen.blit(txt_score1,(300,200))
        self.main_screen.blit(txt_score2,(300,240))
        self.buttons['again'].draw(self.main_screen)
        self.buttons['close'].draw(self.main_screen)
        if self.buttons['close'].is_clicked():             
            pygame.quit() 
            exit()
            pass
        if self.buttons['again'].is_clicked():
            self._init_game()
           # self._game_mode='PLAY'
            


    def _handle_events(self):
        #Serach for event
        self.pressed_key_letter = None
        for event in pygame.event.get(): #it can be called only once
            if event.type == pygame.QUIT:
                pygame.quit() 
                exit()
            if self._game_mode =='PLAY': #only in game_aktiv mode
                if event.type == self.letter_timer:self._genere_letter() #generate Letter 
            if event.type == pygame.KEYDOWN:
                self.pressed_key_letter = pygame.key.name(event.key)

    def _draw(self):
        
        #basic stuff
        self.main_screen.blit(self.grph_background,(0,0))  

        match self._game_mode:
           case 'START': self._start_screen()
           case 'PLAY': self._game_start() 
           case 'END': self._game_end() 


    def run(self):

        while True:
            self._handle_events()
            self._draw()
            self.clock.tick(self.FPS)
            pygame.display.update()

pygame.init()
pygame.display.set_caption("Press a Letter:")

game=Game()
game.run()
        



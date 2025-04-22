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
        self.delete=False
        self.score=False

        self._surface = self.font.render(self._random_letter, True,self.color)
        self.rect = self._surface.get_rect(topleft=(x,y))
    
    def draw(self, screen):
        screen.blit(self._surface, self.rect)
    
    def update_and_move (self,dy,dx=0):
        #move_ip - it moves the same rectangle, it doesn't generate a new one
        self.rect.move_ip(dx,dy)

        if self.rect.bottom > 530:
            self._surface = self.font.render(self._random_letter, True,"RED")
            if self.rect.y > 530: self.delete=True

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.key.key_code(F'{self._random_letter}')]:
                self.delete=True
                self.score=True

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
def genere_letter():
        if len(letters_group)<=max_let_on_screen:
            pos_x=random.choice(columns)
            column_occupied=False
            if len(letters_group)>0:
                for L in letters_group:
                    if L.rect.x == pos_x:
                        column_occupied=True
                        break
                if not column_occupied:
                    letters_group.add(Letter(pos_x))
            else:       
                letters_group.add(Letter(pos_x))
        
def init_game():
    global score, start_time, lives
    score=0
    start_time=(pygame.time.get_ticks())
    lives=3
    letters_group.empty()

pygame.init()
main_screen = pygame.display.set_mode((900,600))
screen_rect = main_screen.get_rect()
main_screen_centrum = screen_rect.center  
pygame.display.set_caption("Press a Letter:")
clock =pygame.time.Clock()

Font1 = pygame.font.Font("fonts/LEMONMILK-LightItalic.otf", 20)
#convert jpg for python to run faster (alpha fill backgrand of the image or smth.)
grph_background = pygame.image.load("graphics/Background.jpg").convert_alpha()

#split screen for collumns -> 30 columns 900/30
columns= [clmn * 30 for clmn in range(30)] #column * 30  column=(0...29) -> 0, 30 ,60, 90
#Group of letters in special pygame containter class Group
letters_group= pygame.sprite.Group()

start_time = 0

btn_start_button = Button("Start Game", pos=main_screen_centrum , font=Font1)
btn_try_again = Button("Try again", pos=(main_screen_centrum[0]-100,main_screen_centrum[1]), font=Font1)
btn_end = Button("Close Game", pos=(main_screen_centrum[0]+100,main_screen_centrum[1]) , font=Font1)
max_let_on_screen=50
letter_timer = pygame.USEREVENT + 1
last_difficult = 0  

game_start=True
game_aktive, game_end=False,False
while True:

    #Basic stuff
    
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    for event in pygame.event.get(): #it can be called only once
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
        if game_aktive: #only in game_aktiv mode
            if event.type == letter_timer:genere_letter() #generate Letter 
        
        
    #Game Star screen
    if game_start:
        main_screen.blit(grph_background,(0,0))
        btn_start_button.draw(main_screen)
        if btn_start_button.is_clicked():
            game_aktive=True
            start_time= pygame.time.get_ticks()
            init_game()
        

    if game_aktive:
        
        current_time = (pygame.time.get_ticks()) - start_time
        main_screen.blit(grph_background,(0,0))
        if current_time < 5000:
            difficult = 1
        elif current_time < 10000:
            difficult = 2
        elif current_time < 20000:
            difficult = 3
        elif current_time < 30000:
            difficult = 4
        print(difficult)

        if difficult != last_difficult: #logik to triger this only once for performance reasons.
            pygame.time.set_timer(letter_timer, int(1000 / difficult))
            last_difficult = difficult

        txt_score = Font1.render((f"Your score: {score}"), True,"black")
        txt_lives = Font1.render((f"Lives: {lives}"), True,"black")


        main_screen.blit(txt_score,(10,550))
        main_screen.blit(txt_lives,(800,550))
        pygame.draw.lines(main_screen, "black",True,[(0, 525),(900, 525)],3)

        #draw all leters form group in a loop
        if letters_group:
            for char in letters_group:    
                if not char.delete:
                    char.draw(main_screen)
                    char.update_and_move(2)
                if char.delete:
                    if char.score:
                        score+=1
                    else:
                        lives-=1
                    letters_group.remove(char)
        #lose condition
        if lives <=0: 
            game_end=True
            game_aktive=False

    if game_end:
        main_screen.blit(grph_background,(0,0))
        txt_score1 = Font1.render(("Your games has ended"), True,"black")
        txt_score2 = Font1.render((f"Your score: {score}"), True,"black")
        main_screen.blit(txt_score1,(300,200))
        main_screen.blit(txt_score2,(300,240))
        btn_try_again.draw(main_screen)
        btn_end.draw(main_screen)

        if btn_end.is_clicked():             
            pygame.quit() 
            exit()
            pass
        if btn_try_again.is_clicked():
            init_game()
            game_end=False
            game_aktive=True


    pygame.display.update()
# with this line a code my game is running with 60fps
    clock.tick(60)



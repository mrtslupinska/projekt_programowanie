import pygame
import random
import math

pygame.init()
pygame.display.set_caption("Cupola")

screen_width = 800
screen_height = 500
#boki ekranu gry - czyli 500-50
margin = 50

screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(pygame.font.get_default_font(), 30)

background = pygame.image.load('/Users/bogna/Desktop/programowanie/gra/lidl.jpg')


#klasy player
class player():
    def __init__(self):
        self.image = pygame.image.load('/Users/bogna/Desktop/programowanie/gra/trolley.png')
        #obecna lokalizacja wozka i to ze pojawia sie na srodku na poczatku gry
        self.x = screen_width/2
        self.y = screen_height-2*margin
        #predkosc z jaka porusza sie wozek
        self.speed = 0.5

    #definicja do zmieniania wartości x playera
    def place_x(self,change):
        self.x += change

    #definicja do zmieniania wartości y playera
    def place_y(self,change):
        self.y += change

    #definicja do zmieniania wartości speed playera
    def speed_change(self,change):
        self.speed += change

#utworzony gracz z klasy
active_player = player()

#lista wgranych obrazkow
fruit_imgs = [pygame.image.load(image) for image in ['/Users/bogna/Desktop/programowanie/gra/apple.png',
'/Users/bogna/Desktop/programowanie/gra/banana.png']]
sweets_imgs = [pygame.image.load(image) for image in ['/Users/bogna/Desktop/programowanie/gra/candy1.png',
'/Users/bogna/Desktop/programowanie/gra/candy2.png']]

#klasa dla wgranych obrazków
class moving_objects():
    def __init__(self):
        self.apple = pygame.image.load('/Users/bogna/Desktop/programowanie/gra/apple.png')
        self.banana = pygame.image.load('/Users/bogna/Desktop/programowanie/gra/banana.png')
        self.candy1 = pygame.image.load('/Users/bogna/Desktop/programowanie/gra/candy1.png')
        self.candy2 = pygame.image.load('/Users/bogna/Desktop/programowanie/gra/candy2.png')
        self.list_of_objects = [[self.apple,self.banana],[self.candy1,self.candy2]]
        self.speed = 5
        self.x = random.randint(0+margin, screen_width-margin)
        self.y = margin

#losowanie spadających obiektów, punkty(wstępnie, do zmiany, nie są zwrócone)
    def get_object(self):
        points =0
        random_number_first = random.randint(0,1)
        random_number_second = random.randint(0,1)
        flying = self.list_of_objects[random_number_first,random_number_second]
        if random_number_first == 0:
            points += 1
        if random_number_second == 1:
            points += -1
        return flying

    def speed(self):
        return self.speed

    def x(self):
        return self.x

    def y(self):
        return self.y


'''#zwraca owoc albo cukierek
def get_object(type="fruit"):
    #lokalizacja owockow i cukierkow
    return {"image" : random.choice(fruit_imgs if type=="fruit" else sweets_imgs),
            "x" : random.randint(0+margin, screen_width-margin),
            "y" : margin,
            "speed" : 5,
            #liczy punkty, 1=owoc, -1=cukierek
            "points": 1 if type=="fruit" else -1}'''


'''#lista spadających cukierków i owoców, pierwszy spada owoc
objects = [get_object("fruit")]'''

objects = moving_objects()

new_object_time = 0
move_object_time = 0
move_object = False

player_movement = 0

running = True
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #w jaki sposob wozek ma sie ruszac
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_movement = -active_player.speed
            if event.key == pygame.K_RIGHT:
                player_movement = active_player.speed
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_movement = 0

    # aktualizacja polozenia wozka w poziomie
    active_player.place_x(player_movement)

    #wozek nie wyjezdza poza ekran
    if active_player.x <= 0:
        active_player.x = 0
    elif active_player.x >= screen_width-2*margin:
        active_player.x = screen_width-2*margin

    # przesuniecie wozka
    screen.blit(active_player.image,(active_player.x,active_player.y))

    # losowosc renderowania owocow i cukierkow
    if new_object_time == 750:
        type = bool(random.getrandbits(1))
        objects.append(get_object)
        new_object_time = 0

    # co ile spadaja owoce i cukierki
    if move_object_time == 25:
        move_object = True
        move_object_time = 0

    #obiekty, ktore sa poza oknem gry
    lost = []

    #renderuje owoce i cukierki
    for i in range(4):
        # przesuwa owoce i cukierki
        if move_object:
            objects.y += objects.speed
        screen.blit(objects.get_object,(objects.x, objects.y))
        # rejestruje obiekty poza oknem gry
        if objects.y >= screen_height:
            lost.append(i)

    # usuwa owoce i cukierki, ktore sa poza ekranem z listy
    new_objects = []
    for i, object in enumerate(objects):
          if i not in lost:
              new_objects.append(object)
    objects = new_objects

    # zapobiega dalszemu przesuwaniu sie owocow i cukierkow
    move_object = False


    # inkrementacja czasu liczników
    new_object_time += 1
    move_object_time += 1

    pygame.display.update()
pygame.quit()

import pygame
import random

pygame.init()
pygame.display.set_caption("Cupola")

screen_width = 900
screen_height = 500
#boki ekranu gry - czyli 500-50
margin = 50

screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(pygame.font.get_default_font(), 30)

background = pygame.image.load('lidl.jpg')

#stworzenie punktacji i życia
points = 0
life = 5

#klasy player
class Player:
    def __init__(self):
        self.image = pygame.image.load('trolley.png')
        #obecna lokalizacja wozka i to ze pojawia sie na srodku na poczatku gry
        self.x = (screen_width-100)/2
        self.y = screen_height-2*margin
        #predkosc z jaka porusza sie wozek
        self.speed = 0.5

    #definicja do zmieniania wartości x playera
    def place_x(self, change):
        self.x += change

    #definicja do zmieniania wartości y playera
    def place_y(self, change):
        self.y += change

    #definicja do zmieniania wartości speed playera
    def speed_change(self, change):
        self.speed += change

#utworzony gracz z klasy
active_player = Player()

fruit_paths = ['apple.png', 'banana.png']
sweets_paths = ['candy1.png', 'candy2.png']

#utworzenie ścieżek obrazków do statusu życia
life_5 = pygame.image.load('heart55.png')
life_4 = pygame.image.load('heart44.png')
life_3 = pygame.image.load('heart33.png')
life_2 = pygame.image.load('heart22.png')
life_1 = pygame.image.load('heart11.png')
life_0 = pygame.image.load('heart00.png')

#lista wgranych obrazkow
fruit_imgs = [[path, pygame.image.load(path)] for path in fruit_paths]
sweets_imgs = [[path, pygame.image.load(path)] for path in sweets_paths]


class MovingObject:

    def __init__(self):
        # wylosować obrazek
        # rozpoznać typ
        self.path = random.choice(fruit_paths + sweets_paths)
        # zwraca nam np. apple
        self.type = self.path.split("/")[-1][0:-4]
        self.x = random.randint(0+margin, (screen_width-100)-margin)
        self.y = margin
        self.speed = 5

        for image in fruit_imgs+sweets_imgs:
            if image[0] == self.path:
                self.img = image[1]

    def x(self):
        return self.x

    def y():
        return self.y

object = MovingObject()

#sprawdzanie kolizji obiektu z wózkiem
'''def Collision(object_x,object_y,trolley_x,trolley_y):
    distance = ((object_x - trolley_x)**2 +
    (object_y - trolley_y)**2)**1/2
    if distance <= 550:
        return True
    else:
        return False'''


#lista spadających cukierków i owoców, pierwszy spada owoc
objects = []

new_object_time = 0
move_object_time = 0
move_object = False

player_movement = 0

running = True
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    #dodanie grafik odpowiadających punktom życia
    if life == 5:
        screen.blit(life_5, (590,88))
    elif life == 4:
        screen.blit(life_4, (590,88))
    elif life == 3:
        screen.blit(life_3, (590,88))
    elif life == 2:
        screen.blit(life_2, (590,88))
    elif life == 1:
        screen.blit(life_1, (590,88))
    elif life <= 0:
        screen.blit(life_0, (590,88))
        life = 0
        move_object = False

    # punktacja - wyświetlanie zdobytych punktów
    score_text = font.render("SCORE: " + str(points), 1,(239,243,255))
    screen.blit(score_text, (600,50))
    #wyświetlanie punktów statusu życia
    life_text = font.render(str(life), 1,(239,243,255))
    screen.blit(life_text, (650,100))

#poruszanie się wózkiem- reakcja na klawisze
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
    elif active_player.x >= (screen_width-100)-2*margin:
        active_player.x = (screen_width-100)-2*margin

    # przesuniecie wozka
    screen.blit(active_player.image, (active_player.x,active_player.y))

    # losowosc renderowania owocow i cukierkow
    if new_object_time == 750:
        type = bool(random.getrandbits(1))
        objects.append(MovingObject())
        new_object_time = 0

    # co ile spadaja owoce i cukierki
    if move_object_time == 25:
        move_object = True
        move_object_time = 0

    #obiekty, ktore sa poza oknem gry
    lost = []
    chaught_objects = []

    #renderuje owoce i cukierki
    for i, object in enumerate(objects):
        # przesuwa owoce i cukierki
        if move_object:
            object.y += object.speed
        screen.blit(object.img, (object.x, object.y))
        # rejestruje obiekty poza oknem gry
        if object.y >= screen_height:
            lost.append(i)

        #sprawdza, czy następuje kolizja i usuwa złapany obiekt
        #(nwm czemu to samo jako def nie działa)
        distance = ((object.x - active_player.x)**2 + (object.y - active_player.y)**2)**1/2
        if distance <= 550:
            lost.append(i)
            chaught_objects.append(i)
            #dodaje punkty po złapaniu owocków
            #i zabezpiecza przed dodawaniem punktów po utracie żyć
            if object.type == "apple" or object.type == "banana":
                if life > 0:
                    points += 1
            #odejmuje życia po złapaniu słodyczy
            else:
                life -= 1



    # usuwa owoce i cukierki, ktore sa poza ekranem z listy
    new_objects = []
    for i, object in enumerate(objects):
          if i not in lost:
              new_objects.append(object)
    objects = new_objects


    '''if object in chaught_objects:
        screen.blit(object.img, (830, 50))'''

    #wyświetla złapane obiekty z boku

    # zapobiega dalszemu przesuwaniu sie owocow i cukierkow
    move_object = False


    # inkrementacja czasu liczników
    new_object_time += 1
    move_object_time += 1



    pygame.display.update()
pygame.quit()

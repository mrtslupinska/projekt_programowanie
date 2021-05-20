import pygame
import random

pygame.init()
pygame.display.set_caption("Cupola")

screen_width = 800
screen_height = 500
#boki ekranu gry - czyli 500-50
margin = 50

screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(pygame.font.get_default_font(), 30)

background = pygame.image.load('/Users/marta/Desktop/gra/lidl.jpg')

#słownik można zmenić na klasy
player = {
        "image": pygame.image.load('/Users/marta/Desktop/gra/trolley.png'),
        #obecna lokalizacja wozka i to ze pojawia sie na srodku na poczatku gry
        "x": screen_width/2,
        "y": screen_height-2*margin,
        #predkosc z jaka porusza sie wozek
        "speed": 0.5
}

#lista wgranych obrazkow
fruit_imgs = [pygame.image.load(image) for image in ['/Users/marta/Desktop/gra/apple.png', '/Users/marta/Desktop/gra/banana.png']]
sweets_imgs = [pygame.image.load(image) for image in ['/Users/marta/Desktop/gra/candy1.png', '/Users/marta/Desktop/gra/candy2.png']]

#zwraca owoc albo cukierek
def get_object(type="fruit"):
    #lokalizacja owockow i cukierkow
    return {"image" : random.choice(fruit_imgs if type=="fruit" else sweets_imgs),
            "x" : random.randint(0+margin, screen_width-margin),
            "y" : margin,
            "speed" : 5,
            #liczy punkty, 1=owoc, -1=cukierek
            "points": 1 if type=="fruit" else -1}

#lista spadających cukierków i owoców, pierwszy spada owoc
objects = [get_object("fruit")]

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
                player_movement = -player["speed"]
            if event.key == pygame.K_RIGHT:
                player_movement = player["speed"]
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_movement = 0

    # aktualizacja polozenia wozka w poziomie
    player["x"] += player_movement

    #wozek nie wyjezdza poza ekran
    if player["x"] <= 0:
        player["x"] = 0
    elif player["x"] >= screen_width-2*margin:
        player["x"] = screen_width-2*margin

    # przesuniecie wozka
    screen.blit(player["image"], (player["x"], player["y"]))

    # losowosc renderowania owocow i cukierkow
    if new_object_time == 750:
        type = bool(random.getrandbits(1))
        objects.append(get_object("fruit" if type else "sweet"))
        new_object_time = 0

    # co ile spadaja owoce i cukierki
    if move_object_time == 25:
        move_object = True
        move_object_time = 0

    #obiekty, ktore sa poza oknem gry
    lost = []

    #renderuje owoce i cukierki
    for i, object in enumerate(objects):
        # przesuwa owoce i cukierki
        if move_object:
            object["y"] += object["speed"]
        screen.blit(object["image"], (object["x"], object["y"]))
        # rejestruje obiekty poza oknem gry
        if object["y"] >= screen_height:
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

import pygame, sys
from pygame.locals import *
import random
import time

pygame.init()
pygame.display.set_caption("Cupola")
pygame.mixer.music.load('music_zapsplat_game_music_arcade_electro_repeating_retro_arp_electro_drums_serious_012.mp3')
pygame.mixer.music.play(-1)
pos_effect = pygame.mixer.Sound('zapsplat_cartoon_musical_riff_cheeky_electric_piano_fast_ascend_66411.mp3')
neg_effect = pygame.mixer.Sound('zapsplat_cartoon_musical_riff_cheeky_electric_piano_descend_66410.mp3')
end_effect = pygame.mixer.Sound('zapsplat_cartoon_descend_med_fast_dual_tone_mallets_002_47930.mp3')
magic_effect = pygame.mixer.Sound('zapsplat_fantasy_magic_glissando_90s_style_dreamy_ascend_006_64936.mp3')
smash_effect = pygame.mixer.Sound('soundible_drop.mp3')
# music and sounds from Zapsplat.com ans soundible

screen_width = 900
screen_height = 500
#boki ekranu gry - czyli 500-50
margin = 50
mouse = pygame.mouse.get_pos()

screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(pygame.font.get_default_font(), 30)
end_font = pygame.font.Font(None, 100)
start_font = pygame.font.Font(None, 80)

# oznaczenia kolorow
BLACK = (0,0,0)
PURPLE = (128,0,128)
colour = PURPLE
FUCHSIA = (255,0,255)
NAVYBLUE = (0,0,128)
BLUE = (0,0,255)
RED = (255,0,0)
RED_1 = (260,0,0)
BLUE_1 = (0,0,170)


background = pygame.image.load('lidl.jpg')

# wybor opcji przed gra
text = start_font.render('QUIT' , True , colour)
text_1 = start_font.render('PLAY' , True , colour)
instruction = pygame.image.load('Instruction.png')

# Przycisk PLAY, nie ma na razie zadnej funkcji, nie wiem jak wywolac nim gre i
# czy czesc z przyciskami moze byc w takiej formie, zeby gra sie odpalila trzeba
# dezaktywowac(?) kod od linijki 49 do 83.

loop = True
while loop:

    for event in pygame.event.get():

        # sprawdza czy klikamy
        if event.type == pygame.MOUSEBUTTONDOWN:

            # konkretne dzialnie w zaleznosci od kliknietej opcji
            if 200 <= mouse[0] <= 350 and 400 <= mouse[1] <= 460:
                pygame.quit()
                running = False
                sys.exit()
            elif 600 <= mouse[0] <= 750 and 400 <= mouse[1] <= 460:
                loop = False

    # wypelnienie tla
    screen.fill((0,0,0))
    # dodanie obrazka z instrukcja
    screen.blit(instruction, (40,40))
    # sprawdzenie pozycji kursora
    pygame.init()
    mouse = pygame.mouse.get_pos()

    # zmaina koloru przycisku w zaleznosci od pozycji kursora
    if 200 <= mouse[0] <= 350 and 400 <= mouse[1] <= 460:
        pygame.draw.rect(screen, BLUE_1, (200,400,150,60))
    elif 600 <= mouse[0] <= 750 and 400 <= mouse[1] <= 460:
        pygame.draw.rect(screen, BLUE_1, (600,400,150,60))
    else:
        pygame.draw.rect(screen, BLUE, (200,400,150,60))
        pygame.draw.rect(screen, BLUE, (600,400,150,60))

    # wyswietlenie tekstu na przyciskach
    screen.blit(text , (220,400))
    screen.blit(text_1, (620,400))

    pygame.display.update()

# funkcja specjalnego efektu tekstu
def display_text_animation(string):
    text = ''
    for char in range(len(string)):
        screen.fill((0,0,0))
        text += string[char]
        chosen_text = end_font.render(text, True, (colour))
        text_rect = chosen_text.get_rect(center = (screen_width/2, screen_height/2))
        screen.blit(chosen_text, text_rect)
        pygame.display.update()
        pygame.time.wait(200)

# funkcja wyswietlajaca wynik koncowy
def end_screen():
    screen.fill((0,0,0))
    score_text_2 = end_font.render('YOUR SCORE: '  +  str(points), 1, colour)
    screen.blit(score_text_2, (150, 350))
    screen.blit(life_0, (590,88))
    screen.blit(life00, (300,50))
    pygame.display.update()
    pygame.time.wait(4000)

# funkcja pokazująca +1/-0,1 na ekranie, gdy zdobędzie/straci się się punkt
def show_added_points(points):
    text = points
    chosen_text = end_font.render(text, True, (255,255,255))
    text_rect = chosen_text.get_rect(center = (850, 200))
    screen.blit(chosen_text, text_rect)
    pygame.display.update()
    pygame.time.wait(150)


#stworzenie punktacji i życia
points = round(0,2)
life = 5
apple_points = 0
banana_points = 0
pear_points = 0
orange_points = 0


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

fruit_paths = ['apple.png','banana.png','pear.png','orange.png']
sweets_paths = ['candy1.png','candy2.png','candy.png','candy-2.png']


#utworzenie ścieżek obrazków do statusu życia
life_max = pygame.image.load('strong6.png')
life_5 = pygame.image.load('heart55.png')
life_4 = pygame.image.load('heart44.png')
life_3 = pygame.image.load('heart33.png')
life_2 = pygame.image.load('heart22.png')
life_1 = pygame.image.load('heart11.png')
life_0 = pygame.image.load('heart00.png')
life00 = pygame.image.load('yayy.png')

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
    if life > 5:
        screen.blit(life_max, (590,88))
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


    # punktacja - wyświetlanie zdobytych punktów
    score_text = font.render("SCORE: " + str(round(points,2)), 1,(239,243,255))
    screen.blit(score_text, (600,50))
    #wyświetlanie punktów statusu życia
    life_text = font.render(str(life), 1,(239,243,255))
    screen.blit(life_text, (650,100))

    #dodanie przyspieszenia gracza i zwolnienia po stracie życia
    if points >= 6:
        active_player.speed = 0.7
    if points >= 10:
        active_player.speed = 0.8
    if points >= 15:
        active_player.speed = 0.9
    if points >= 20:
        active_player.speed = 0.95
    if points >= 25:
        active_player.speed = 1.1
    if life <= 0:
        active_player.speed = 0.1
        # wyswietlenie wyniku koncowego
        end_screen()
        # zmiana dzwiekow po przegraniu
        pygame.mixer.music.stop()
        end_effect.play()
        # ekran koncowy
        display_text_animation('GAME OVER')
        pygame.time.wait(600)
        pygame.quit()
        running = False
        sys.exit()

#dodanie przyspieszenia spadania obiektów i zwolnienia po utracie życia
    if points >= 4:
        object.speed = 7
    if points >= 6:
        object.speed = 8
    if points >= 13:
        object.speed = 9
    if points >= 20:
        object.speed = 10
    if points >= 25:
        object.speed = 11
    if points >= 30:
        object.speed = 12
    if points >= 35:
        object.speed = 13
    if life <= 0:
        object.speed = 1

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
            chaught_objects.append(i)
            screen.blit(object.img, (830, 250))
            #dodaje punkty po złapaniu owocków
            #i zabezpiecza przed dodawaniem punktów po utracie żyć
            if object.type == "apple" or object.type == "banana" or object.type == 'pear' or object.type == 'orange':
                if life > 0:
                    points += 1
                    show_added_points('+1')
                    # odtwarza dany efekt dzwiekowy po zlapaniu owocu
                    pos_effect.play()

#funkcja magiczna, liczy punkty dla każdego owocka i daje extra 3 punkty
#za złapanie 7 owoców z danego rodzaju, co dodaje też jedno extra życie
#oraz odtwarza dany dzwiek
                    if object.type == "apple":
                        apple_points +=1
                        if apple_points == 7:
                            magic_effect.play()
                            points += 3
                            life +=1
                        if apple_points > 7:
                            apple_points = 0


                    if object.type == "banana":
                        banana_points +=1
                        if banana_points == 7:
                            magic_effect.play()
                            points += 3
                            life += 1
                        if banana_points >7:
                            banana_points = 0

                    if object.type == "pear":
                        pear_points +=1
                        if pear_points == 7:
                            magic_effect.play()
                            points += 3
                            life += 1
                        if pear_points >7:
                            pear_points = 0

                    if object.type == "orange":
                        orange_points +=1
                        if orange_points == 7:
                            magic_effect.play()
                            points += 3
                            life += 1
                        if orange_points >7:
                            orange_points = 0

            else:
                life -= 1
                #wstrzymuje obraz gry po złapaniu cukierka i utracie punktu
                time.sleep(0.3)
                # odtwarza dany efekt dzwiekowy po zlapaniu cukierka
                neg_effect.play()

    #odejmuje 0,1 punkta, gdy nie złapiemy owoców
    for i, object in enumerate(objects):
        if i in lost and i not in chaught_objects:
            if object.type == "apple" or object.type == "banana" or object.type == 'pear' or object.type == 'orange':
                points += - 0.1
                smash_effect.play()
                show_added_points('-0.1')


    # usuwa owoce i cukierki, ktore sa poza ekranem z listy
    new_objects = []
    for i, object in enumerate(objects):
          if i not in lost and i not in chaught_objects:
              new_objects.append(object)
    objects = new_objects


    # zapobiega dalszemu przesuwaniu sie owocow i cukierkow
    move_object = False


    # inkrementacja czasu liczników
    new_object_time += 1
    move_object_time += 1



    pygame.display.update()
pygame.quit()

import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((612, 367))  # окно игры и его размер
pygame.display.set_caption("MegaMen VS Zombie")  # название игры
pygame.display.set_icon(pygame.image.load('images/icon.png'))  # загрузка иконки

bg = pygame.image.load('images/bg.jpg').convert_alpha()  # загрузка бэка

# таймер
zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer, 2500)  # таймер появления зоми

label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)  # шрифты
point = pygame.font.Font('fonts/Roboto-Black.ttf', 30)  # шрифты

lose_label = label.render('Вы проиграли!', False, (193, 196, 199))  # надписи
restart_label = label.render('Играть заново', False, (115, 132, 148))  # надписи
restart_label_rect = restart_label.get_rect(topleft=(180, 200))  # отображение надписи

ammo = pygame.image.load('images/ammo.png').convert_alpha()  # загрузка картинки и патронов
stone = pygame.image.load('images/stone.png').convert_alpha()  # загрузка картинки и патронов
shot = pygame.image.load('images/shot.png').convert_alpha()
zombie_dead = pygame.image.load('images/zombie_dead.png').convert_alpha()

shots_left = 10  # счетчик потронов
shots = []
zombie_d = 0  # счетчик зомби
ammmo_p = 0

gameplay = True

# Игрок двидение
walk_left = [
    pygame.image.load('images/left/left1.png').convert_alpha(),
    pygame.image.load('images/left/left2.png').convert_alpha(),
    pygame.image.load('images/left/left3.png').convert_alpha(),
    pygame.image.load('images/left/left4.png').convert_alpha(),
    pygame.image.load('images/left/left5.png').convert_alpha(),
    pygame.image.load('images/left/left6.png').convert_alpha(),
    pygame.image.load('images/left/left7.png').convert_alpha(),
    pygame.image.load('images/left/left8.png').convert_alpha(),
    pygame.image.load('images/left/left9.png').convert_alpha(),
    pygame.image.load('images/left/left10.png').convert_alpha()
]

walk_right = [
    pygame.image.load('images/right/right1.png').convert_alpha(),
    pygame.image.load('images/right/right2.png').convert_alpha(),
    pygame.image.load('images/right/right3.png').convert_alpha(),
    pygame.image.load('images/right/right4.png').convert_alpha(),
    pygame.image.load('images/right/right5.png').convert_alpha(),
    pygame.image.load('images/right/right6.png').convert_alpha(),
    pygame.image.load('images/right/right7.png').convert_alpha(),
    pygame.image.load('images/right/right8.png').convert_alpha(),
    pygame.image.load('images/right/right9.png').convert_alpha(),
    pygame.image.load('images/right/right10.png').convert_alpha(),
]

# анимация зомби
zombie_walk = [
    pygame.image.load('images/zombie_walk/zombie1.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie2.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie3.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie4.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie5.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie6.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie7.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie8.png').convert_alpha(),
    pygame.image.load('images/zombie_walk/zombie9.png').convert_alpha()
]

# zombie = pygame.image.load('images/zombie.png').convert_alpha()

zombie_list_in_game = []

player_anim_count = 0
zombie_anim_count = 0

bg_x = 0

player_speed = 10
player_x = 150
player_y = 248
is_jump = False
jump_count = 8

# звуки
bg_sound = pygame.mixer.Sound('sounds/bg.mp3')
bg_sound.play(-1).set_volume(0.5)
defeat_sound = pygame.mixer.Sound('sounds/defeat.mp3')
shot_sound = pygame.mixer.Sound('sounds/shoot.mp3')
zombie_dam = pygame.mixer.Sound('sounds/enemydamage.mp3')

running = True
while running:

    # фон и его передвижение
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 612, 0))
    bg_x -= 4
    if bg_x == -612:
        bg_x = 0

    if gameplay:

        # отображение инфы и прочего
        shots_left_render = point.render(str(shots_left), False, (0, 0, 0))
        screen.blit(shots_left_render, (40, 0))
        screen.blit(ammo, (0, 0))
        screen.blit(zombie_dead, (510, 0))
        zombie_d_render = point.render(str(zombie_d), False, (0, 0, 0))
        screen.blit(zombie_d_render, (550, 0))
        screen.blit(stone, (0, 282))
        stones = screen.blit(stone, (0, 282))
        # ammmo_p_render = point.render(str(ammmo_p), False, (0, 0, 0))
        # screen.blit(ammmo_p_render, (300, 0))

        player_rect = walk_left[0].get_rect(
            topleft=(player_x, player_y))  # переменная для отработки столкновиний с играком

        # цикл обработки столкнавений с зомби
        if zombie_list_in_game:
            for (i, el) in enumerate(zombie_list_in_game):
                screen.blit(zombie_walk[zombie_anim_count], el)
                el.x -= 10
                if el.x < -10:
                    zombie_list_in_game.pop(i)
                if player_rect.colliderect(el):
                    defeat_sound.play()
                    gameplay = False
                if stones.colliderect(el):
                    ammmo_p += 1

        # получение доп патронов
        if ammmo_p >= 25 and ammmo_p % 25 == 0:
            screen.blit(ammo, (300, 278))
            ammmo_pi = screen.blit(ammo, (300, 278))
            if player_rect.colliderect(ammmo_pi):
                shots_left += 1

        # управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 12:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 540:
            player_x += player_speed
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 9:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if zombie_anim_count == 8:
            zombie_anim_count = 0
        else:
            zombie_anim_count += 1

        # цикл столкновения с выстрелом

        if shots:
            for (i, el) in enumerate(shots):
                screen.blit(shot, (el.x, el.y))
                el.x += 20

                if el.x > 630:
                    shots.pop(i)

                if zombie_list_in_game:
                    for (index, zombie_el) in enumerate(zombie_list_in_game):
                        if el.colliderect(zombie_el):
                            zombie_dam.play()
                            zombie_list_in_game.pop(index)
                            shots.pop(i)
                            zombie_d += 1



    # случаи поражения и рестарта
    # надписи поражения и рестарта
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        # cам рестрат и обнудение счетчиков
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            zombie_list_in_game.clear()
            shots.clear()
            shots_left = 10
            zombie_d = 0
            ammmo_pi = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # спам замбей
        if event.type == zombie_timer:
            zombie_list_in_game.append(zombie_walk[zombie_anim_count].get_rect(topleft=(640, 247)))
        # ограничение патронов и само их появление
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and shots_left > 0:
            shot_sound.play()
            shots.append(shot.get_rect(topleft=(player_x + 60, player_y + 13)))
            shots_left -= 1

    clock.tick(15)  # скорость игры

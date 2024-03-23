import random
import sys
import pygame
import random as r


width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Undertale')
heart_image = pygame.image.load('./data1/heart.png')
box_width, box_height = 204, 204
box_x, box_y = (width - box_width) // 2 + 2, (height - box_height) // 2
heart_width, heart_height = 16, 16
heart_speed = 5
clock = pygame.time.Clock()

pygame.mixer.init()
heat_sound = pygame.mixer.Sound('./data1/snd_curtgunshot.ogg')
spider_song = pygame.mixer.Sound('./data1/mus_spider.ogg')
text_sound = pygame.mixer.Sound('./data1/text.mp3')

pygame.font.init()
big_font = pygame.font.Font('./data1/Minecraft Rus NEW.otf', 40)
small_font = pygame.font.Font('./data1/Minecraft Rus NEW.otf', 20)


class Player(pygame.sprite.Sprite):
    default_heart = pygame.image.load('./data1/heart.png')
    immortal_heart = pygame.image.load('./data1/immortal_heart.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Player.default_heart
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = box_x + (box_width // 2) - 5, box_y + (box_height // 2) - 5
        self.immortal = False
        self.immortal_timer = None
        self.immortal_duration = 2000
        self.hp = 5

    def update(self, move):
        if move == 'left':
            self.rect = self.rect.move(-4, 0)
        if move == 'right':
            self.rect = self.rect.move(4, 0)
        if move == 'down':
            self.rect = self.rect.move(0, 4)
        if move == 'up':
            self.rect = self.rect.move(0, -4)

    def heat(self):
        if pygame.sprite.spritecollideany(self, attack1) and not self.immortal:
            self.immortal = True
            self.immortal_timer = pygame.time.get_ticks()
            self.image = Player.immortal_heart
            heat_sound.play()
            self.hp -= 1

        if self.immortal:
            current_time = pygame.time.get_ticks()
            if current_time - self.immortal_timer >= self.immortal_duration:
                self.immortal = False
                self.image = Player.default_heart

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def set_x(self, move):
        self.rect.x = move

    def set_y(self, move):
        self.rect.y = move

    def get_hp(self):
        return self.hp


class AttackBar(pygame.sprite.Sprite):
    def __init__(self, group, x=335, y=530):
        super().__init__(group)
        self.image = pygame.image.load('./data1/trash.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class AttackLine(pygame.sprite.Sprite):
    def __init__(self, group, x=335, y=530):
        super().__init__(group)
        self.image = pygame.image.load('./data1/line.png')
        self.rect = self.image.get_rect()
        self.default_x = x
        self.rect.x, self.rect.y = x, y
        self.vx = 3

    def update(self):
        self.rect.x += self.vx

    def reset(self):
        self.rect.x = self.default_x

    def get_x(self):
        return self.rect.x


class Attack1(pygame.sprite.Sprite):
    def __init__(self, group, vector):
        super().__init__(group)
        self.vector = vector
        self.name = 'peaks'
        self.image = pygame.image.load(f'./data1/attack_sprite1_{vector}.png')
        self.rect = self.image.get_rect()
        if self.vector == 'down':
            self.rect.x = r.randint((width - box_width) // 2, (width - box_width) // 2 + 180)
            self.rect.y = (height - box_height) // 2 + 5
        elif self.vector == 'up':
            self.rect.x = r.randint((width - box_width) // 2, (width - box_width) // 2 + 180)
            self.rect.y = (box_height + box_y)
        elif self.vector == 'right':
            self.rect.x = box_x
            self.rect.y = r.randint(box_y, box_y + 170)
        elif self.vector == 'left':
            self.rect.x = box_x + 200 - 30
            self.rect.y = r.randint(box_y, box_y + 170)

    def update(self):
        if self.vector == 'down':
            self.rect = self.rect.move(0, 3)
        elif self.vector == 'up':
            self.rect = self.rect.move(0, -3)
        elif self.vector == 'right':
            self.rect = self.rect.move(3, 0)
        elif self.vector == 'left':
            self.rect = self.rect.move(-3, 0)

    def get_vector(self):
        return self.vector

    def get_name(self):
        return self.name


class Attack2(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.name = 'ball'
        self.image = pygame.image.load('./data1/attack_sprite2.png')
        self.rect = self.image.get_rect()
        self.vx = 0
        self.touch = 0
        self.broken = 4
        while self.vx == 0:
            self.vx = r.randint(-2, 2)
        pos = r.randint(0, 1)
        if pos == 0:
            self.rect.x = r.randint(box_x + 20, box_x + box_width - 20)
            self.rect.y = box_y + 3
            self.vy = 2
        elif pos == 1:
            self.rect.x = r.randint(box_x + 20, box_x + box_width - 20)
            self.rect.y = box_y + box_height - 15
            self.vy = r.randint(-2, -1)

    def update(self):
        if self.touch >= 3:
            self.broken += 1
        if self.broken % 5 == 0:
            self.image = pygame.image.load(f'./data1/broken_ball{self.broken // 5}.png')
            self.broken += 1
        if self.broken < 5:
            if self.rect.x <= box_x or self.rect.x >= box_x + box_width - 14:
                self.vx *= -1
                self.touch += 1
            elif self.rect.y <= box_y + 2 or self.rect.y >= box_y + box_height - 14:
                self.vy *= -1
                self.touch += 1
            self.rect = self.rect.move(self.vx, self.vy)

    def get_name(self):
        return self.name

    def get_touch(self):
        return self.touch

    def get_broken(self):
        return self.broken


class Attack3(pygame.sprite.Sprite):
    def __init__(self, group, y, move):
        super().__init__(group)
        self.name = 'bone'
        self.image = pygame.image.load('./data1/bone.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = box_x + 200, y
        self.move = move
        if self.move == 'right':
            self.vx = 3
            self.rect.x, self.rect.y = box_x, y
        elif self.move == 'left':
            self.rect.x, self.rect.y = box_x + 200, y
            self.vx = -3

    def update(self):
        self.rect.x += self.vx

    def get_name(self):
        return self.name

    def get_vector(self):
        return self.move


class Attack4(pygame.sprite.Sprite):
    def __init__(self, group, x, y, posx, posy):
        super().__init__(group)
        self.name = 'block'
        self.image = pygame.image.load('./data1/block.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + posx * 20, y - posy * 20
        self.vy = 3
        self.posx, self.posy = posx, posy
        self.is_update = True
        self.is_blink = 1
        self.is_ban = False
        self.blink_count = 0

    def update(self):
        if not self.is_update:
            return
        block = 0
        for i in tetris:
            if i[self.posx] == 1:
                block += 1
            else:
                break
        if self.rect.y <= box_y + box_height - 23 - 20 * block:
            self.rect.y += self.vy
        else:
            tetris[self.posy][self.posx] = 1
            self.is_update = False

    def blink(self):
        if self.is_blink == 1:
            self.image = pygame.image.load('./data1/empty_block.png')
            self.blink_count += 1
        else:
            self.image = pygame.image.load('./data1/block.png')

        if self.blink_count == 3:
            self.is_ban = True
        self.is_blink *= -1

    def get_name(self):
        return self.name

    def get_is_ban(self):
        return self.is_ban


class DrawEnemy(pygame.sprite.Sprite):
    def __init__(self, group, name, x=(box_x + box_width // 2 - 90), y=100):
        super().__init__(group)
        self.a = 1
        self.name = name
        self.count_frames = 2
        if self.name.lower() == 'nerdlin':
            self.image_text = './data1/Nerdlin'
            self.image = pygame.image.load(f'{self.image_text}{self.count_frames}.png')
        elif self.name.lower() == 'ghost':
            self.image_text = './data1/ghost1'
            self.image = pygame.image.load(f'{self.image_text}.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        if self.name.lower() == 'ghost':
            return
        if self.a % 30 == 0 and self.count_frames == 1:
            self.count_frames = 2
        elif self.a % 30 == 0 and self.count_frames == 2:
            self.count_frames = 1
        path = f'{self.image_text}{self.count_frames}.png'
        self.image = pygame.image.load(path)
        self.a += 1


class EmptyEnemy:
    def __init__(self):
        self.a = 0
        self.is_attacking = False
        self.name = ''
        self.hp = 20

    def attack01(self):
        pass

    def attack02(self):
        pass

    def end_attack(self):
        self.a = 0
        self.is_attacking = False

    def get_is_attacking(self):
        return self.is_attacking

    def set_is_attacking(self, new):
        self.is_attacking = new

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def set_hp(self, new):
        self.hp = new


class Enemy1(EmptyEnemy):
    def __init__(self):
        super().__init__()
        self.name = 'Nerdlin'

    def attack01(self):
        if self.a == 0:
            for i in range(4, 6):
                Attack4(attack1, box_x + 2, box_y + 1, i, 0)
            Attack4(attack1, box_x + 2, box_y + 1, 4, 1)
        if self.a == 5:
            for i in range(3):
                Attack4(attack1, box_x + 2, box_y + 1, i, 0)
            Attack4(attack1, box_x + 2, box_y + 1, 0, 1)
        if self.a == 10:
            Attack4(attack1, box_x + 2, box_y + 1, 3, 0)
            for i in range(1, 4):
                Attack4(attack1, box_x + 2, box_y + 1, i, 1)
        if self.a == 15:
            for i in range(4):
                Attack4(attack1, box_x + 2, box_y + 1, i, 2)
        if self.a == 20:
            for i in range(6, 8):
                Attack4(attack1, box_x + 2, box_y + 1, i, 0)
            for i in range(5, 7):
                Attack4(attack1, box_x + 2, box_y + 1, i, 1)
        if self.a == 25:
            for i in range(8, 10):
                Attack4(attack1, box_x + 2, box_y + 1, i, 0)
            for i in range(7, 9):
                Attack4(attack1, box_x + 2, box_y + 1, i, 1)
        if self.a == 30:
            Attack4(attack1, box_x + 2, box_y + 1, 9, 1)
            for i in range(7, 10):
                Attack4(attack1, box_x + 2, box_y + 1, i, 2)
        if self.a == 35:
            for i in range(4, 7):
                Attack4(attack1, box_x + 2, box_y + 1, i, 2)
        if self.a >= 43 and self.a % 2 == 0:
            for i in attack1:
                if i.get_name() == 'block':
                    i.blink()
        if self.a >= 54:
            self.end_attack()
        self.a += 1

    def attack02(self):
        move_list = ['up', 'down', 'left', 'right']
        if self.a <= 16:
            Attack1(attack1, r.choice(move_list))
            self.a += 1
        if len(attack1) == 0:
            self.end_attack()


class Enemy2(EmptyEnemy):
    def __init__(self):
        super().__init__()
        self.name = 'Ghost'

    def attack01(self):
        if self.a <= 16 and self.a % 2 == 0:
            Attack2(attack1)
        self.a += 1
        if len(attack1) == 0:
            self.end_attack()

    def attack02(self):
        if self.a <= 16 and self.a % 2 == 0:
            pos = r.randint(110, 250)
            Attack3(attack1, pos, 'left')
            Attack3(attack1, pos + 230, 'left')
        self.a += 1
        if len(attack1) == 0:
            self.end_attack()


attack1 = pygame.sprite.Group()
tetris = [[0] * 10 for i in range(3)]



player = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
attack_bar_group = pygame.sprite.Group()
line_group = pygame.sprite.Group()
heart = Player(player)
a = 1
pike = pygame.USEREVENT
pygame.time.set_timer(pike, 200)
enemy = EmptyEnemy()
choice_attack = 0
attack_bar = AttackBar(attack_bar_group)
line = AttackLine(line_group)

enemy_text = small_font.render('', True, 'white')
big_text = big_font.render('', True, 'white')
damage_text = small_font.render('', True, 'white')
enemy_hp = small_font.render('', True, 'white')
player_hp = small_font.render('', True, 'white')

first_attack = False
player_attacking = False
draw_big_text = True
draw_attack_bar = False
enemy_attack_time = True
before_len_attack = 0
running = True

while running:
    screen.fill('black')
    if heart.get_hp() <= 0:
        attack1.empty()
        spider_song.stop()
    elif enemy.get_hp() <= 0:
        attack1.empty()
        spider_song.stop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            attack1.empty()
            spider_song.stop()
        if event.type == pike:
            a += 1
            if a == 2:
                choice_enemy = r.randint(1, 2)
                if choice_enemy == 1:
                    enemy = Enemy1()
                    DrawEnemy(enemy_sprite, enemy.get_name(), box_x + box_width // 2 - 90, 100)
                elif choice_enemy == 2:
                    enemy = Enemy2()
                    DrawEnemy(enemy_sprite, enemy.get_name(), box_x + box_width // 2 - 90, -20)
                spider_song.play(loops=-1)

                enemy_text = small_font.render(f'На вас напал: {enemy.get_name()}', True, 'white')
                big_text = big_font.render('НАЖМИТЕ [X] ЧТО БЫ ПРИНЯТЬ БОЙ', True, 'white')

            if enemy.get_is_attacking():
                if choice_attack == 1:
                    enemy.attack01()
                if choice_attack == 2:
                    enemy.attack02()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(pygame.mouse.get_pos())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.update('left')
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.update('right')
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.update('up')
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.update('down')

    if keys[pygame.K_q] and player_attacking:
        draw_attack_bar = True
        player_attacking = False
        enemy_attack_time = False
        big_text = big_font.render('НАЖМИТЕ [E] КАК МОЖНО БЛИЖЕ К ЦЕНТРУ', True, 'white')

    if (keys[pygame.K_e] and draw_attack_bar) or (draw_attack_bar and line.get_x() >= 880):
        draw_attack_bar = False
        big_text = big_font.render('НАЖМИТЕ [X] ЧТО БЫ ПРИНЯТЬ БОЙ', True, 'white')
        enemy_attack_time = True
        damage = 0
        if line.get_x() in range(810, 900) or line.get_x() in range(330, 420):
            damage = 1
        elif line.get_x() in range(420, 520) or line.get_x() in range(700, 810):
            damage = 3
        elif line.get_x() in range(520, 700):
            damage = 6
        line.reset()
        enemy.set_hp(enemy.get_hp() - damage)
        damage_text = small_font.render(f'ВЫ НАНЕСЛИ {damage} УРОНА', True, 'white')

    if keys[pygame.K_x] and not enemy.get_is_attacking() and enemy_attack_time:
        enemy.set_is_attacking(True)
        choice_attack = r.randint(1, 2)
        big_text = big_font.render('', True, 'white')
        enemy_attack_time = False
        damage_text = small_font.render(f'', True, 'white')

    if heart.get_x() < box_x:
        heart.set_x(box_x + 2)
    if heart.get_x() > box_x + box_width - heart_width:
        heart.set_x(box_x + box_width - heart_width - 2)
    if heart.get_y() < box_y:
        heart.set_y(box_y + 2)
    if heart.get_y() > box_y + box_height - heart_height:
        heart.set_y(box_y + box_height - heart_height - 2)
    pygame.draw.rect(screen, 'white', (box_x, box_y, box_width, box_height), 2)

    ban_attack = []
    for i in attack1:
        if i.get_name() == 'peaks':
            if i.get_vector() == 'down' and i.rect.y >= 270:
                ban_attack.append(i)
            elif i.get_vector() == 'up' and i.rect.y <= box_y:
                ban_attack.append(i)
            elif i.get_vector() == 'right' and i.rect.x >= box_x + 170:
                ban_attack.append(i)
            elif i.get_vector() == 'left' and i.rect.x <= box_x:
                ban_attack.append(i)

        elif i.get_name() == 'bone':
            if i.get_vector() == 'right' and i.rect.x >= box_x + 195:
                ban_attack.append(i)
            elif i.get_vector() == 'left' and i.rect.x <= box_x:
                ban_attack.append(i)

        elif i.get_name() == 'ball':
            if i.get_broken() >= 15:
                ban_attack.append(i)

        elif i.get_name() == 'block':
            if i.get_is_ban():
                ban_attack.append(i)
                tetris = [[0] * 10 for i in range(3)]
    for i in ban_attack:
        attack1.remove(i)

    if before_len_attack != 0 and len(attack1) == 0:
        enemy.end_attack()
        enemy.set_is_attacking(False)
        before_len_attack = 0
        big_text = big_font.render(f'НАЖМИТЕ [Q] ЧТО БЫ АТАКОВАТЬ', True, 'white')
        player_attacking = True

    else:
        before_len_attack = len(attack1)

    if draw_attack_bar:
        attack_bar_group.draw(screen)
        line_group.update()
        line_group.draw(screen)

    enemy_hp = small_font.render(f'HP {enemy.get_name()}: {enemy.get_hp()}/20',
                                 True, 'white')
    player_hp = small_font.render(f'ВАШИ HP: {heart.get_hp()}', True, 'white')

    player.draw(screen)
    attack1.draw(screen)
    enemy_sprite.draw(screen)

    heart.heat()

    attack1.update()
    enemy_sprite.update()

    screen.blit(enemy_text, (50, 50))
    screen.blit(big_text, (100, 700))
    screen.blit(damage_text, (470, 520))
    screen.blit(enemy_hp, (730, 310))
    screen.blit(player_hp, (730, 480))

    pygame.display.flip()
    clock.tick(60)


if __name__ == '__main__':
    undertale()
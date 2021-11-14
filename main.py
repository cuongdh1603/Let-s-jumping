#gọi thư viện pygame
import pygame, sys
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy

#khởi tạo chương trình pygame
pygame.init()
#các hằng số kích thước cửa sổ 
SCREEN_WIDTH = 400 #chiều rộng màn hình
SCREEN_HEIGHT = 600 #chiều cao màn hình
#tạo ra màn hình window 
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Let's jumping") #tạo tên tiêu đề cho màn hình
#Đặt tốc độ khung hình 
clock = pygame.time.Clock()
FPS = 60 #frame per second
#Định dạng màu 
WHITE = (255,255,255) #màu trắng 
LIGHT_BLUE =  (77,166,255) #màu xanh
BLACK = (0,0,0)
PANEL = (0,100,0) #(153,217,234)
RED = (255,0,0)
GREEN = (115,179,72)
#Định dạng phông:
font_small = pygame.font.SysFont('Roboto',20)
font_medium = pygame.font.SysFont('Roboto',24)
font_big = pygame.font.SysFont('Roboto',36)
font_Sbig = pygame.font.SysFont('Roboto',48)
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    text_rect = img.get_rect(center=(SCREEN_WIDTH/2, y))
    screen.blit(img,text_rect)
def draw_text1(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
#panel truyền điểm số hiện tại 
kt = [True, True, True]
def draw_panel():
    global kt
    pygame.draw.rect(screen,PANEL,(0,0,SCREEN_WIDTH,25))
    pygame.draw.line(screen,WHITE,(0,25),(SCREEN_WIDTH,25),0)
    draw_text1(f'SCORE: {score}',font_medium,WHITE,5,5) #LIGHT_BLUE
    if score > highest_score[0]:
        draw_text1("YOU ARE NUMBER ONE!!!",font_medium,WHITE,190,5)
        if So and kt[0]:
            wow.play()
            kt[0] = False
    elif score > highest_score[1]:
        draw_text1("YOU ARE IN TOP 2!!!",font_medium,WHITE,200,5)
        if So and kt[1]:
            wow.play()
            kt[1] = False
    elif score > highest_score[2]:
        draw_text1("YOU ARE IN TOP 3!!!",font_medium,WHITE,200,5)
        if So and kt[2]:
            wow.play()
            kt[2] = False
    elif score > 1500:
        draw_text1("GREAT!!!",font_medium,WHITE,300,5)

#hằng số trọng lực
GRAVITY = 1
#Lăn background
SCROLL_THRESH = 200
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter_close = 0
top = 4
fade_counter_open = SCREEN_WIDTH//2
highest_score = [] #Điểm cao nhất từng được chơi(được lưu lại trong highest_score.txt)
if os.path.exists('highest_score.txt'):
    with open('highest_score.txt','r') as f:
        highest_score = [int(i) for i in f.readlines()]
highest_score.sort(reverse=True)
#Khai báo các đối tượng hình ảnh
background_image = pygame.image.load('property/bg.png').convert_alpha() #ảnh nền
player_image = pygame.image.load('property/jump.png').convert_alpha() #ảnh người chơi
platform_image = pygame.image.load('property/wood.png').convert_alpha() #

#Khai báo sprites 
bird_sheet_img = pygame.image.load('property/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)

#hàm vẽ background
def draw_bg(bg_scroll):
    screen.blit(background_image,(0,0+bg_scroll))
    screen.blit(background_image,(0,-600+bg_scroll))

# Khởi tạo biến âm thanh
Mu = True
So = True
music = mixer.Sound('Sound/Music.mp3')
music.set_volume(0.2)
move = mixer.Sound('Sound/Move.mp3')
move.set_volume(0.5)
jump = mixer.Sound('Sound/Jump.mp3')
hit = mixer.Sound('Sound/Hit.mp3')
death = mixer.Sound('Sound/Death.mp3')
wow = mixer.Sound('Sound/Wow.mp3')
clap = mixer.Sound('Sound/Clap.mp3')
clap.set_volume(0.5)
#-----------------------NGƯỜI CHƠI------------------------------------
class Player():
    #hàm khởi tạo:
    def __init__(self, x, y) :
        self.image = pygame.transform.scale(player_image,(45,45)) #thay đổi kích thước 
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0,0,self.width,self.height) #khởi tạo hình chữ nhật có (0,0) là điểm trên cùng bên trái,(self.width,self.height) là điểm dưới cùng bên phải
        self.rect.center = (x,y) #đặt trọng tâm hình chữ nhật tại điểm (x,y)
        self.vel_y = 0 # vận tốc của người chơi 
        self.flip = False #lật ảnh khi move , đặt mặc định ảnh gốc (không lật)
    #xử lý lệnh nhận từ bàn phím:
    def move(self):
        scroll = 0
        dx = 0
        dy = 0 #ban đầu đang ở phía dưới 
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
            if So:
                move.play()
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
            if So:
                move.play()
        self.vel_y += GRAVITY 
        dy += self.vel_y
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        for platform in platform_group:
            #nếu như xảy ra va chạm giữa người chơi và platform...kiểm tra hướng va chạm 
            if platform.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                #nếu như người chơi ở vị trí trên platform:
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        if So:
                            jump.play()
        #kiểm tra nếu người chơi đã nhảy lên cạnh trên của màn hình
        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy
        #thay đổi vị trí người chơi
        self.rect.x += dx
        self.rect.y += dy + scroll
        return scroll
    #hiển thị đối tượng ra màn hình:
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),(self.rect.x-12,self.rect.y-5))
        # pygame.draw.rect(screen,0,self.rect,1)
#-----------------------------------------------------------------------------------  
#Người chơi
player = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT-150)
#Tạo ra nhóm sprite 
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
#---------------------------------PLATFORM------------------------------------------
MAX_PLATFORMS = 10
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width,moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image,(width,10))
        self.moving = moving
        self.move_counter = random.randint(0,50)
        self.direction = random.choice([-1,1])
        self.speed = random.randint(1,2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,scroll):
        # dịch chuyển platform sang hai bên khi nó là moving platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        if self.move_counter >= 100 or self.rect.left<0 or self.rect.right>SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        #thay đổi tọa độ y của platform
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
#------------------------------------------------------------------------------------
platform_group = pygame.sprite.Group()
#create starting platform
platform = Platform(SCREEN_WIDTH//2-50,SCREEN_HEIGHT-50,100,False)
platform_group.add(platform)

def mapGame():
    global game_over, bg_scroll, fade_counter_open, score, fade_counter_close, highest_score, platform,top
    if game_over == False:
        #lồng background
        scroll = player.move()
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)
        if fade_counter_open > 0:
            fade_counter_open -= 5
            pygame.draw.rect(screen,WHITE,(0,0,fade_counter_open,SCREEN_HEIGHT))
            pygame.draw.rect(screen,WHITE,(SCREEN_WIDTH-fade_counter_open,0,SCREEN_WIDTH,SCREEN_HEIGHT))

        # print(score)
        #khởi tạo các platform 
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40,80)
            p_x = random.randint(0,SCREEN_WIDTH-p_w)
            p_y = platform.rect.y - random.randint(80,120)
            p_type = random.randint(1,2)
            if p_type == 1 and score > 1500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x,p_y,p_w,p_moving)
            platform_group.add(platform)
        #sửa đổi platform
        platform_group.update(scroll)

        #khởi tạo enemies
        if len(enemy_group) == 0 and score >= 1500: #and score > 1500:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)

        #sửa đổi enemies
        enemy_group.update(scroll, SCREEN_WIDTH)

        #tăng điểm 
        if scroll > 0:
            score += scroll
        platform_group.draw(screen)

        #vẽ sprites
        platform_group.draw(screen)
        enemy_group.draw(screen)

        #vẽ bảng điểm
        draw_panel()
        #vẽ hình ảnh người chơi
        player.draw()
        #kiểm tra thua cuộc 
        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
            if So:
                death.play()
        if pygame.sprite.spritecollide(player, enemy_group, False): #kiểm tra va chạm
            if pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                if So:
                    hit.play()
                    death.play()
                enemy_group.empty()
                platform_group.empty()
    else:
        if fade_counter_close < SCREEN_WIDTH:
            fade_counter_close += 5
            pygame.draw.rect(screen,WHITE,(0,0,fade_counter_close,SCREEN_HEIGHT//6))
            pygame.draw.rect(screen,WHITE,(SCREEN_WIDTH-fade_counter_close,SCREEN_HEIGHT//6,fade_counter_close,SCREEN_HEIGHT//6))
            pygame.draw.rect(screen,WHITE,(0,SCREEN_HEIGHT//3,fade_counter_close,SCREEN_HEIGHT//6))
            pygame.draw.rect(screen,WHITE,(SCREEN_WIDTH-fade_counter_close,SCREEN_HEIGHT//2,fade_counter_close,SCREEN_HEIGHT//6))
            pygame.draw.rect(screen,WHITE,(0,SCREEN_HEIGHT//6*4,fade_counter_close,SCREEN_HEIGHT//6))
            pygame.draw.rect(screen,WHITE,(SCREEN_WIDTH-fade_counter_close,SCREEN_HEIGHT//6*5,fade_counter_close,SCREEN_HEIGHT//6))
        else:
            score_p = 3
            for i in range(2,-1,-1):
                if score > highest_score[i]:
                    score_p = i
            for i in range(2,score_p,-1):
                highest_score[i] = highest_score[i-1]
            if score_p<3: highest_score[score_p] = score
            top = score_p + 1
            with open('highest_score.txt','w') as f:
                for i in highest_score:
                    f.write(str(i))
                    f.write('\n')
            print(top)
            while True:
                clock.tick(FPS)
                mapGameOver()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                        pygame.quit()
                        sys.exit()
                pygame.display.update()

def InputImage(filename, x, y):
    return pygame.transform.scale(pygame.image.load(filename).convert(), (x, y))

def Clicked(sprite):
    mouseState = pygame.mouse.get_pressed()
    if not mouseState[0]:
        return False  # not pressed
    pos = pygame.mouse.get_pos()
    if sprite.collidepoint(pos):
        return True
    else:
        return False


def mapMenu():
    screen.fill(WHITE)
    screen.blit(Play, P_Re)
    screen.blit(Setting, S_Re)
    screen.blit(Rank, R_Re)
    screen.blit(Guide, G_Re)
    screen.blit(Exit, E_Re)
    if Clicked(P_Re):
        print("Play")
        while True:
            clock.tick(FPS)
            mapGame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    elif Clicked(S_Re):
        while True:
            clock.tick(FPS)
            mapSettings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    elif Clicked(R_Re):
        print("Rank")
        #Cho bang xep diem cao
        while True:
            clock.tick(FPS)
            mapRank()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    elif Clicked(G_Re):
        print("Guide")
        #Cho bang huong dan
        while True:
            clock.tick(FPS)
            mapGuide()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    elif Clicked(E_Re):
        #Thoat chuong trinh
        pygame.quit()
        sys.exit()

def mapSettings():
    global So, Mu
    screen.fill((WHITE))
    screen.blit(Board, B_Re)
    if So:
        screen.blit(SoOn, SOn_Re)
    else:
        screen.blit(SoOff, SOf_Re)
    if Mu:
        screen.blit(MuOn, Mun_Re)
    else:
        screen.blit(MuOff, Muf_Re)
    screen.blit(Ret, Re_Re)
    if Clicked(SOn_Re) or Clicked(SOf_Re):
        So = not So
        print(So)
    if Clicked(Mun_Re) or Clicked(Muf_Re):
        Mu = not Mu
        print(Mu)
        if Mu:
            music.play()
        else:
            music.stop()
    if Clicked(Re_Re):
        while True:
            clock.tick(FPS)
            mapMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    
def mapRank():
    screen.fill((WHITE))
    screen.blit(Board, B_Re)
    draw_text(f'HIGH SCORE',font_Sbig,WHITE,80,100)
    draw_text(f'TOP 1:   {highest_score[0]}',font_big,WHITE,0,150)
    draw_text(f'TOP 2:   {highest_score[1]}',font_big,WHITE,0,200)
    draw_text(f'TOP 3:   {highest_score[2]}',font_big,WHITE,0,250)
    screen.blit(Ret, Re_Re)
    if Clicked(Re_Re):
        while True:
            clock.tick(FPS)
            mapMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    

def mapGameOver():
    screen.fill((WHITE))
    screen.blit(Board, B_Re)
    draw_text('GAME OVER',font_Sbig,RED,0,80)
    draw_text(f'SCORE',font_big,RED,0,200)
    draw_text(f'{score}',font_Sbig,RED,0,250)
    if top < 4:
        draw_text(f'You are in top {top}',font_big,WHITE,0,125)
        draw_text(f'Congratulation!',font_big,WHITE,0,155)
        if So:
            clap.play()
    screen.blit(Restart, Res_Re)
    screen.blit(Home, H_Re)
    screen.blit(Exit, E2_Re)
    if Clicked(E2_Re):
        #Thoat chuong trinh
        pygame.quit()
        sys.exit() 
    if Clicked(Res_Re):
        clap.stop()
        set()
        print("Play")
        while True:
            clock.tick(FPS)
            mapGame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    if Clicked(H_Re):
        clap.stop()
        set()
        while True:
            clock.tick(FPS)
            mapMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

def mapGuide():
    screen.fill((WHITE))
    screen.blit(GuideText,GT_Re)
    Re2_Re = Ret.get_rect(center = (200, 550))
    screen.blit(Ret, Re2_Re)
    draw_text(f'GUIDE',font_Sbig,WHITE,0,50)
    if Clicked(Re2_Re):
        while True:
            clock.tick(FPS)
            mapMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
                    pygame.quit()
                    sys.exit()
            pygame.display.update()  

def set():
    global game_over, score, scroll, fade_counter_close, fade_counter_open, platform_group, platform, kt
    game_over = False
    score = 0
    scroll = 0
    fade_counter_close = 0
    fade_counter_open = SCREEN_WIDTH//2
    #reset player
    player.rect.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT-150)
    #reset platform
    platform_group.empty()
    #create starting platform
    platform = Platform(SCREEN_WIDTH//2-50,SCREEN_HEIGHT-50,100,False)
    platform_group.add(platform)
    kt = [True, True, True]

# Khai báo các đối tượng ảnh
Play = InputImage(("images\play.png"), 250, 60)
P_Re = Play.get_rect(center = (200, 100))
Setting = InputImage(("images\Setting.png"), 250, 60)
S_Re = Setting.get_rect(center = (200, 200))
Rank = InputImage(("images\Rank.png"), 250, 60)
R_Re = Rank.get_rect(center = (200, 300))
Guide = InputImage(("images\Guide.png"), 250, 60)
G_Re = Guide.get_rect(center = (200, 400))
Exit = InputImage(("images\quit.png"), 250, 60)
E_Re = Exit.get_rect(center = (200, 500))

Board = InputImage(("images\Board.png"), 300, 340)
B_Re = Board.get_rect(center = (200, 210))

SoOn = InputImage(("images\SoundOn.png"), 250, 60)
SOn_Re = SoOn.get_rect(center = (200, 160))
SoOff = InputImage(("images\SoundOff.png"), 250, 60)
SOf_Re = SoOff.get_rect(center = (200, 160))
MuOn = InputImage(("images\MusicOn.png"), 250, 60)
Mun_Re = MuOn.get_rect(center = (200, 260))
MuOff = InputImage(("images\MusicOff.png"), 250, 60)
Muf_Re = MuOff.get_rect(center = (200, 260))
Ret = InputImage(("images\Return.png"), 250, 60)
Re_Re = Ret.get_rect(center = (200, 370))

Restart = InputImage(("images\Restart.png"), 250, 60)
Res_Re = Restart.get_rect(center = (200, 370))
Home = InputImage(("images\Home.png"), 250, 60)
H_Re = Ret.get_rect(center = (200, 440))
E2_Re = Exit.get_rect(center = (200, 510))

GuideText = InputImage(("images\GuideText.png"), 300, 550)
GT_Re = GuideText.get_rect(center = (200, 280))
# ****************************************************************************************  
               
#vòng lặp 
while True:
    clock.tick(FPS)
    if Mu:
        music.play() 
    mapMenu()
    #xử lý các sự kiện từ phía người chơi 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# nếu như người chơi muốn tắt màn hình  
            pygame.quit()
            sys.exit()
    #cập nhật lại màn hình window
    pygame.display.update()
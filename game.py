'''
參考程式：https://blog.techbridge.cc/2019/10/19/how-to-build-up-game-with-pygame-tutorial/
　　　　　https://codertw.com/程式語言/370103/
遊戲規則：蟑螂每0.5秒更換位置，打到蟑螂時加2分，分數無上限
'''
import pygame, sys, random
from pygame.locals import QUIT, MOUSEBUTTONDOWN, USEREVENT

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
IMAGE_WIDTH = 150
IMAGE_HEIGHT = 200
BG_COLOR = (200, 200, 200) # 淺灰色
FONT_COLOR = (0, 0, 0) # 黑色
MOUSE_IMAGE = './images/slipper.png'
ROACH_IMAGE = './images/cockroach.png'
MOUSE_SIZE = (150, 200)
FPS = 60

class Cockroach(pygame.sprite.Sprite): # 建立Cockroach類別（繼承pygame.sprite.Sprite）
    def __init__(self, width, height, rand_x, rand_y, window_w, window_h):
        super().__init__()
        self.raw_image = pygame.image.load(ROACH_IMAGE).convert_alpha() # 載入圖片
        self.image = pygame.transform.scale(self.raw_image, (width, height)) # 變更圖片大小
        self.rect = self.image.get_rect() # 回傳位置
        self.rect.topleft = (rand_x, rand_y) # 定位

        self.width = width
        self.height = height
        self.window_w = window_w
        self.window_h = window_h

def get_rand_pos(window_w, window_h, image_w, image_h): # 產生隨機位置
    rand_x = random.randint(image_w, window_w - image_w)
    rand_y = random.randint(image_h, window_h - image_h)
    return rand_x, rand_y

def main():
    pygame.init()
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Cockroach Killer') # 遊戲標題
    
    mouse_raw_image = pygame.image.load(MOUSE_IMAGE).convert_alpha() # 拖鞋圖片
    mouse_image = pygame.transform.scale(mouse_raw_image, (MOUSE_SIZE))

    random_x, random_y = get_rand_pos(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_WIDTH, IMAGE_HEIGHT)
    cockroach = Cockroach(IMAGE_WIDTH, IMAGE_HEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
    reload_roach_event = USEREVENT + 1
    pygame.time.set_timer(reload_roach_event, 500)

    point = 0
    my_font = pygame.font.SysFont(None, 60)
    main_clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get(): # 偵測事件
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == reload_roach_event: # 偵測重新整理事件，固定時間移除蟑螂，換新位置
                cockroach.kill()
                random_x, random_y = get_rand_pos(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_WIDTH, IMAGE_HEIGHT) # 蟑螂新位置
                cockroach = Cockroach(IMAGE_WIDTH, IMAGE_HEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
            elif event.type == MOUSEBUTTONDOWN: # 當使用者點擊滑鼠時，檢查滑鼠座標是否有在蟑螂圖片上
                if random_x < pygame.mouse.get_pos()[0] < random_x + IMAGE_WIDTH and random_y < pygame.mouse.get_pos()[1] < random_y + IMAGE_HEIGHT:
                    random_x, random_y = get_rand_pos(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_WIDTH, IMAGE_HEIGHT)
                    cockroach = Cockroach(IMAGE_WIDTH, IMAGE_HEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
                    point += 2 # 加2分

        pygame.mouse.set_visible(False) # 隱藏滑鼠
        mouse_x, mouse_y = pygame.mouse.get_pos() # 滑鼠座標
        mouse_x -= mouse_image.get_width() / 2
        mouse_y -= mouse_image.get_height() / 2

        window_surface.fill(BG_COLOR) # 設定背景顏色
        text_surface = my_font.render('Points: %d' % point, True, FONT_COLOR) # 遊戲分數
        window_surface.blit(cockroach.image, cockroach.rect) # 渲染圖片與文字
        window_surface.blit(text_surface, (20, 20))
        window_surface.blit(mouse_image, (mouse_x, mouse_y)) # 用拖鞋圖片取代滑鼠

        pygame.display.update()
        main_clock.tick(FPS) # 控制遊戲迴圈迭代速率

if __name__ == '__main__':
    main()

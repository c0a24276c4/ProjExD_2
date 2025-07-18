import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = { #移動用辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判断結果、縦方向判断結果）
    両面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    bb2_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(bb2_img, (0, 0, 0,), pg.Rect(0, 0, WIDTH, HEIGHT))
    bb2_img.set_alpha(200)
    screen.blit(bb2_img, (0, 0))
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [425, 275])
    bg2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(bg2_img, [375, 275])
    bg3_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(bg3_img, [740,275])
    pg.display.update()
    time.sleep(5)

def init_bb_items() -> tuple[list[pg.Surface],list[int]]:
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r) #追加機能途中
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #赤に円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() #Rectする
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5 
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv(0), -sum_mv(0))
        screen.blit(kk_img, kk_rct)

        bb_imgs, bb_accs = init_bb_items() 
        avx = vx*bb_accs[min(tmr//500,9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1 
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

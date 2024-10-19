from pygame import *

from spriteClass import GameSprite

''' colors '''
background = (200, 255, 255)

window = display.set_mode((700, 500))
window.fill(background)

clock = time.Clock()

''' variables '''
game = True

'''' game loop '''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    platform_left.reset(window_object=window)
    platform_right.reset(window_object=window)
    ball.reset(window_object=window)

    display.update()
    clock.tick(60)
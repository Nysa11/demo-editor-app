from pygame import *
from SpriteClass import GameSprite, Player

''' colors '''
background = (200, 255, 255)

# Create a window
window = display.set_mode((700, 500))
window.fill(background)

# Create instances of players or platforms with the correct paths
platform_left = Player("img/slider.jpg", 50, 200, 5, 55, 80)  # Update to point to slider.jpg
platform_right = Player("img/slider.jpg", 600, 200, 5, 55, 80)  # Update to point to slider.jpg
ball = GameSprite("img/ball.jpg", 350, 250, 0, 30, 30)  # Update to point to ball.jpg

clock = time.Clock()

''' variables '''
game = True

'''' game loop '''
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    # Update player positions
    platform_left.update_left()
    platform_right.update_right()

    # Fill the window with the background color
    window.fill(background)

    # Reset all sprites
    platform_left.reset(window_object=window)
    platform_right.reset(window_object=window)
    ball.reset(window_object=window)

    # Update the display
    display.update()
    clock.tick(60)

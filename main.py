from pygame import *
from SpriteClass import GameSprite, Player

''' colors '''
background = (200, 255, 255)

# Create a window
window = display.set_mode((700, 500))
window.fill(background)

# Create instances of players or platforms
platform_left = Player("path_to_left_platform_image.png", 50, 200, 5, 55, 80)  # Adjust parameters accordingly
platform_right = Player("path_to_right_platform_image.png", 600, 200, 5, 55, 80)  # Adjust parameters accordingly
ball = GameSprite("path_to_ball_image.png", 350, 250, 0, 30, 30)  # Adjust parameters accordingly

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

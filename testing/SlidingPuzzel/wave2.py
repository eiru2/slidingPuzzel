# Source - https://stackoverflow.com/a/62336993
# Posted by Kingsley, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-06, License - CC BY-SA 4.0

import pygame
  
# Window size
WINDOW_WIDTH    = 400
WINDOW_HEIGHT   = 400

### initialisation
pygame.init()
window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
pygame.display.set_caption("Gradient Rect")

def gradientWaves( window, left_colour, right_colour, points ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) ,pygame.SRCALPHA)                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( WINDOW_WIDTH, WINDOW_HEIGHT) )  # stretch!
    x,y = colour_rect.get_size()
    print(x,y)
    mask_surface = pygame.Surface((x, y), pygame.SRCALPHA)

# Define your polygon points (relative to the image size)

    
    pygame.draw.polygon(mask_surface, (255, 255, 255, 255), points)
    
    colour_rect.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    
    window.blit( colour_rect, (0,0) )                                    # paint it


### Main Loop
clock = pygame.time.Clock()
finished = False
while not finished:

    # Handle user-input
    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            finished = True

    # Update the window
    window.fill( ( 0,0,0 ) )
    #gradientRect( window, (0, 255, 0), (0, 100, 0), pygame.Rect( 100,100, 100, 50 ) )
    gradientRect( window, (255, 255, 0), (0, 0, 255), ((100,100) , (200,100), (200,200)) )
    # pygame.draw.polygon(window,(0,0,0),((100,100) , (200,100), (200,200)))
    pygame.display.flip()

    # Clamp FPS
    clock.tick_busy_loop(60)

pygame.quit()

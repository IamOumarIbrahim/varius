import sys
import pygame
from game_engine import GameEngine

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    
    # Set up screen
    screen_width = 1024
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cave Survivor: Tsushima Stances")
    
    # Initialize engine
    engine = GameEngine(screen)
    
    # Run main game loop
    engine.run()
    
    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import pygame
import cv2
import sys
import time
from snake_game import SnakeGame
from hand_tracker import HandTracker

def main():
    pygame.init()
    
    # Constants
    WIDTH, HEIGHT = 640, 480
    FPS = 60
    GAME_UPDATE_DELAY = 0.15 # Seconds between snake moves
    
    # Setup Display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hand Gesture Snake")
    clock = pygame.time.Clock()
    
    # Setup Game and Tracker
    game = SnakeGame(WIDTH, HEIGHT)
    tracker = HandTracker()
    
    # Setup Camera
    cap = cv2.VideoCapture(0)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)
    
    last_move_time = time.time()
    current_gesture = None
    
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 2. Camera & Hand Tracking
        success, img = cap.read()
        if not success:
            print("Failed to capture video")
            break
            
        img = cv2.flip(img, 1) # Mirror view
        
        # Find hands and get gesture
        img = tracker.find_hands(img)
        gesture = tracker.get_gesture_direction(img)
        
        if gesture:
            current_gesture = gesture

        # 3. Update Game Logic
        if time.time() - last_move_time > GAME_UPDATE_DELAY:
            game.update(current_gesture)
            last_move_time = time.time()

        # 4. Rendering
        
        # Convert OpenCV image to Pygame Surface
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.transpose(img_rgb) # Pygame uses (width, height) but numpy is (row, col)
        # Actually numpy is (y, x, c), pygame surface expects (x, y) for blit if we create from buffer correctly
        # The easiest way:
        img_surface = pygame.surfarray.make_surface(img_rgb)
        
        # Note: make_surface expects (width, height, 3), but cv2 image is (height, width, 3).
        # So we need to swap axes.
        
        screen.blit(img_surface, (0, 0))
        
        # Draw Game Elements on top (with some transparency if possible, or just solid)
        # To make it look "AR", we can draw the snake directly on the screen surface which now has the video
        game.draw(screen)
        
        # Draw Gesture Debug Info
        if current_gesture:
            font = pygame.font.SysFont('arial', 30)
            text = font.render(f"Gesture: {current_gesture}", True, (255, 255, 0))
            screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    cap.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.prev_pos = None
        self.min_swipe_dist = 15 # Reduced from 40 to make it more sensitive

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_gesture_direction(self, img):
        """
        Determines direction based on the velocity (swipe) of the index finger.
        Fast movement triggers a direction. Slow movement is ignored (allows resetting).
        """
        if not self.results.multi_hand_landmarks:
            self.prev_pos = None
            return None

        # Get the first hand detected
        hand_lms = self.results.multi_hand_landmarks[0]
        
        # Use Index Finger Tip (landmark 8)
        landmark = hand_lms.landmark[8] 
        
        h, w, c = img.shape
        cx, cy = int(landmark.x * w), int(landmark.y * h)

        direction = None

        if self.prev_pos:
            px, py = self.prev_pos
            dx = cx - px
            dy = cy - py
            
            # Check if movement is fast enough to be a swipe
            if abs(dx) > self.min_swipe_dist or abs(dy) > self.min_swipe_dist:
                if abs(dx) > abs(dy):
                    # Reverting to standard: dx > 0 is RIGHT movement on screen
                    if dx > 0: direction = "RIGHT" 
                    else: direction = "LEFT"
                else:
                    if dy > 0: direction = "DOWN"
                    else: direction = "UP"
                
                # Draw swipe line
                cv2.line(img, (px, py), (cx, cy), (0, 255, 0), 3)
            else:
                # Draw trail for slow movement
                cv2.line(img, (px, py), (cx, cy), (0, 0, 255), 1)

        self.prev_pos = (cx, cy)
        
        # Draw the tracking point
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return direction

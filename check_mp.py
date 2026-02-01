import mediapipe as mp
print(f"Mediapipe version: {mp.__version__}")
try:
    print(f"Mediapipe solutions: {mp.solutions}")
    print("Success!")
except AttributeError as e:
    print(f"Error: {e}")
    print(f"Attributes of mp: {dir(mp)}")

import cv2
import numpy as np
from mss import mss
from PIL import Image

mon = {'top': 0, 'left':283, 'width':800, 'height':700}

# Create a "screen capture" object to capture video from the screen
sct = mss()

frames = []
def record():
    while True:
        # Capture a frame from the screen
        sct_img = sct.grab(mon)
        img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Add the frame to the list of captured frames
        frames.append(img_bgr)
        
        # Display the frame
        cv2.imshow('test', img_bgr)
        
        # Break out of the loop if the user presses the "q" key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()

# Define the replay function
def replay():
    # Set the frame rate of the replay
    frame_rate = 30
    
    # Display the frames in the list
    for frame in frames:
        cv2.imshow('test', frame)
        
        # Break out of the loop if the user presses the "q" key
        if cv2.waitKey(1000 // frame_rate) & 0xFF == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()


# # Call the replay function
# record()
# replay()

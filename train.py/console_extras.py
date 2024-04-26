import time
import sys
import threading

# Animation function
def loading_animation():
    animation = "|/-\\"
    while not stop_animation:  # Loop until the animation is stopped
        for frame in animation:
            if stop_animation:
                break
            sys.stdout.write("\r" + frame)
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\rDone!     ")

# Start the animation in a separate thread
def start_animation():
    global stop_animation
    stop_animation = False
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()
    return animation_thread

# Stop the animation
def stop_animation(animation_thread):
    global stop_animation
    stop_animation = True
    animation_thread.join()

# Example usage
animation_thread = start_animation()
# Simulate some work
time.sleep(5)
stop_animation(animation_thread)
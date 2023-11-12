
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 30

time_speed = 1



def increase_speed():
    global time_speed
    if time_speed < 1 :
        time_speed += 0.25
    elif time_speed < 10:
        time_speed += 0.5
    return time_speed
        
def decrease_speed():
    global time_speed
    if time_speed > 1:
        time_speed -= 0.5
    elif time_speed > 0.25 :
        time_speed -= 0.25
    return time_speed

    




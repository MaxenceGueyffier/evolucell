playground_width = 2000
playground_height = 1200

screen_width = 1000
screen_height = 600

initial_qtt_of_food = int(500*((playground_width/screen_width)**2))

fps = 30
time_speed = 1

def increase_speed():
    global time_speed
    global fps
    if time_speed < 1 :
        time_speed += 0.25
    elif time_speed < 5 :
        time_speed += 0.5
    elif fps == 30 :
        fps = 60
    return time_speed
        
def decrease_speed():
    global time_speed
    global fps
    if fps == 60 :
        fps = 30
    elif time_speed > 1:
        time_speed -= 0.5
    elif time_speed > 0.25 :
        time_speed -= 0.25
    
    return time_speed

    




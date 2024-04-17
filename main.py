import time


study_time = 25*60
break_time = 5*60
study_sessions = 4
long_break_time = 15*60

def countdown(time_in_seconds):
    while time_in_seconds:
        mins, secs = divmod (time_in_seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins,secs)
        print(timer, end="\r")
        time.sleep(1)
        time_in_seconds -= 1
    print("Fire in the hole")

countdown(study_time)

import time
import os
import json
import argparse

def countdown(time_in_seconds):
    while time_in_seconds:
        mins, secs = divmod(time_in_seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        time_in_seconds -= 1
    print("Fire in the hole")

def toggle_timer(start_timer, args):
    start_timer = not start_timer
    args.toggle = False
    return start_timer

def check_current_state(args, start_timer):
    if args.start:
        start_timer = True
    if args.pause:
        start_timer = False
    if args.toggle:
        start_timer = toggle_timer(start_timer, args)
    return start_timer

def main():
    study_time = 25*60
    break_time = 5*60
    study_sessions = 4
    long_break_time = 15*60
    start_timer = True      # True while countdown is running, False when paused

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="Start the timer", action="store_true")
    parser.add_argument("-p", "--pause", help="Pause the timer", action="store_true")
    parser.add_argument("-r", "--reset", help="Reset the timer", action="store_true")
    parser.add_argument("-t", "--toggle", help="Toggle the timer", action="store_true")

    start_timer = check_current_state(parser.parse_args(), start_timer)

    print("Start: ", start_timer)
    print("Reset: ", parser.parse_args().reset)

    if start_timer == True and parser.parse_args().reset == False:
        countdown(study_time)

if __name__ == "__main__":
    main()

import time
import os
import json
import argparse

default_config = {
        "study_time": 25 * 60,
        "break_time": 5 * 60,
        "study_sessions": 4,
        "long_break_time": 15 * 60,
        "last_paused_at": 0,            # Placeholder for time when timer was paused
        "countdown_running": False,   # Placeholder for checking current state of timer
        }

config_filename = "config.json"

# Creating default config.json if it doesn't exist
def create_default_json(config_filename):
    with open(config_filename, 'w') as config_file:
        json.dump(default_config, config_file, indent= 4)

def countdown(time_in_seconds):
    while time_in_seconds:
        mins, secs = divmod(time_in_seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        time_in_seconds -= 1
    print("Fire in the hole")

def toggle_timer(countdown_running, args):
    countdown_running = not countdown_running
    args.toggle = False
    return countdown_running

def check_current_state(args, countdown_running):
    if args.start:
        countdown_running = True
    if args.pause:
        countdown_running = False
    if args.toggle:
        countdown_running = toggle_timer(countdown_running, args)
    return countdown_running

def main():
    # Check for file existence and create default config if it doesn't exist
    if not os.path.isfile(config_filename):
        create_default_json(config_filename)

    # Load config from config.json
    try:
        with open(config_filename, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = default_config

    study_time = config["study_time"]
    break_time = config["break_time"]
    study_sessions = config["study_sessions"]
    long_break_time = config["long_break_time"]
    countdown_running = config["countdown_running"]      # True while countdown is running, False when paused

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="Start the timer", action="store_true")
    parser.add_argument("-p", "--pause", help="Pause the timer", action="store_true")
    parser.add_argument("-r", "--reset", help="Reset the timer", action="store_true")
    parser.add_argument("-t", "--toggle", help="Toggle the timer", action="store_true")

    countdown_running = check_current_state(parser.parse_args(), countdown_running)

    if countdown_running == True and parser.parse_args().reset == False:
        countdown(study_time)

if __name__ == "__main__":
    main()

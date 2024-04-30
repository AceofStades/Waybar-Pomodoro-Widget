import time
import os
import json
import argparse
import threading
import queue
import sys

default_config = {
        "study_time": 25 * 60,
        "break_time": 5 * 60,
        "study_sessions": 4,
        "long_break_time": 15 * 60,
        "last_paused_at": 0,            # Placeholder for time when timer was paused
        "state_running": False,         # Placeholder for checking current state of timer
        }

config_filename = "config.json"

# Creating default config.json if it doesn't exist
def create_default_json(config_filename):
    with open(config_filename, 'w') as config_file:
        json.dump(default_config, config_file, indent= 4)
    config_file.close()

# Countdown timer
def countdown(time_in_seconds, state_running):
    while time_in_seconds:
        if state_running == False:
            update_last_paused_at(time_in_seconds)
            break
        else:
            try:
                mins, secs = divmod(time_in_seconds, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                time_in_seconds -= 1
            except KeyboardInterrupt:
                update_last_paused_at(time_in_seconds)
                break

# Toggle the timer between running and paused states
# def toggle_timer(state_running, args):
#     state_running = not state_running
#     args.toggle = False
#     return state_running

# Check the current state of the timer
# def check_current_state(args, state_running):
#     if args.start:
#         state_running = True
#     if args.pause:
#         state_running = False
#     if args.toggle:
#         state_running = toggle_timer(state_running, args)
#     return state_running

def check_current_state(state_queue, state_running, study_time):
    if state_queue == "s":
        state_running = True
    if state_queue == "p":
        state_running = False
    if state_queue == "t":
        state_running = not state_running
    if state_running == "r":
        state_running = False
        update_last_paused_at(study_time)   # Reset the timer to study_time for now. Will implement reset to current_session_time later
    return state_running

# Updates the last_paused_at time in config.json if the timer is paused
def update_last_paused_at(time_in_seconds):
    with open(config_filename, 'r') as config_file_read:
        config = json.load(config_file_read)
        config["last_paused_at"] = time_in_seconds
        with open(config_filename, 'w') as config_file_write:
            json.dump(config, config_file_write, indent=4)
        config_file_write.close()
    config_file_read.close()

def main(state_queue):
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
    state_running = config["state_running"]      # True while countdown is running, False when paused
    last_paused_at = config["last_paused_at"]

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-s", "--start", help="Start the timer", action="store_true")
    # parser.add_argument("-p", "--pause", help="Pause the timer", action="store_true")
    # parser.add_argument("-r", "--reset", help="Reset the timer", action="store_true")
    # parser.add_argument("-t", "--toggle", help="Toggle the timer", action="store_true")

    # state_running = check_current_state(parser.parse_args(), state_running)

    state_running = check_current_state(state_queue, state_running, study_time)

    if last_paused_at == 0:
        countdown(study_time, state_running)
    else:
        countdown(last_paused_at, state_running)

if __name__ == "__main__":
    state_queue = queue.Queue()
    threading.Thread(target=main, daemon=True, args=(state_queue,)).start()
    while True:
        state = char(input())
        if state in ("s", "p", "r", "t"):
            state_queue.put(state)

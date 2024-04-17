import time
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


def main():
    study_time = 25*60
    break_time = 5*60
    study_sessions = 4
    long_break_time = 15*60

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--start", help="Start the timer", action="store_true")
    parser.add_argument("-p", "--pause", help="Pause the timer", action="store_false", dest="start")
    parser.add_argument("-r", "--reset", help="Reset the timer", action="store_true")
    parser.add_argument("-t", "--toggle", help="Toggle the timer", action="store_true")

    def toggle_timer(args):
        args.start = not args.start
        return args

    if parser.parse_args().toggle:
        toggle_timer(parser.parse_args())

    print("Start: ", parser.parse_args().start)
    print("Reset: ", parser.parse_args().reset)


if __name__ == "__main__":
    main()

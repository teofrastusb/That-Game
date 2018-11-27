from runners.single_match import Runner
from timer.timer import timed

def main():
    runner = Runner('PlayerCode')
    timed(runner.run)()

if __name__ == "__main__":
    main()


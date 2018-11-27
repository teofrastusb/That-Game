from runners.replay import Runner

def main():
    runner = Runner('PlayerCode', './recordings/2018-11-26_21h11m30s__6-pack-attack__vs__bite-or-move-randomly.txt')
    runner.run()

if __name__ == "__main__":
    main()
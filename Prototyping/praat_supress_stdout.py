import multiprocessing

def spawn():
    print('Spawned')

if __name__ == '__main__':
    for i in range(100):
        p = multiprocessing.Process(target=spawn)
        p.start()
    p.join()
    print('finished')

"""
p = subprocess.Popen(['./praat', '--run', 'Individual0.praat'])
p.communicate()

"""
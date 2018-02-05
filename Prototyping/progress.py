from tqdm import tqdm
import time, os


ha = 2

for i in tqdm(range(10)):
    
    ha += 2
    time.sleep(1)
    print(ha)
    #os.system('cls' if os.name == 'nt' else 'clear')
    for i in tqdm(range(5)):
        time.sleep(0.5)

    
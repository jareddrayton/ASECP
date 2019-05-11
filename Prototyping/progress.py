from tqdm import tqdm
import time, os


ha = 2

for i in tqdm(range(5)):
    
    ha += 2
    time.sleep(0.3)
    print(ha)
    #os.system('cls' if os.name == 'nt' else 'clear')
    for i in tqdm(range(5)):
        time.sleep(0.5)

    
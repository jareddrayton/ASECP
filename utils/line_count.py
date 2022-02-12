import glob

total = 0

for f in glob.glob('..\\*\\*.py'):
    with open(f, 'r', encoding="latin-1") as fi:
        total += len(fi.readlines())

print(total)

def remove_duplicate_samples(file_path):
    with open('{}'.format(file_path), 'r') as f:
        lines = f.readlines()

        
    print(len(lines))
    print(len(set(lines)))

    lines = set(lines)

    with open('pp_{}'.format(file_path), 'w') as f:
        new_set = set()
        for line in lines:
            param = ''.join(line.split(',')[0:27])
            if param not in new_set:
                new_set.add(param)
                f.write(line)

remove_duplicate_samples('labelled_logfbank_data.txt')
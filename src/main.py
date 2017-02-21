def fetch_tet_values(fileName):
    dictionary = {}
    with open(fileName) as f:
        for line in f:
            entries = line.split(',')
            for entry in entries:
                char = entry[0]
                index = 0
                while(not (char.isalpha())):
                    index+=1
                    if(index == len(entry)):
                        break;
                    char = entry[index]
                if(index < len(entry)):
                    key = entry[index:(index + 4)]
                    val = entry[(index + 4):entry.rfind('\'')]
                    dictionary[key] = float(val)
    return dictionary

print(fetch_tet_values('probabilities.txt'))

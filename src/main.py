from random import randint

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

tet_table = [0] * (26*26*26*26)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
buff = []
plain_text = []
max_trials = 10000000
sq = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10,11,12,13,14],[15, 16, 17, 18, 19],[20,21,22,23,24]]
inv_row = [0]*91
inv_col = [0]*91
fudge_factor = 0.2
buf_len = 0
tet_vals = fetch_tet_values('probabilities.txt')
def create_table(string):
    #TODO: make the table using string's chars.
    global tet_table
    string = string.upper()
    max_value = 0
    max_table_len = 26 * 26 * 26 * 26
    c0 = string[0]
    c1 = string[1]
    c2 = string[2]
    n0 = alphabet.index(c0)
    n1 = alphabet.index(c1)
    n2 = alphabet.index(c2)
    for i in range(3, len(string)):
        c = string[i]
        n = alphabet.index(c)
        x = n0 + 26*n1 + 26 * 26 * n2 + 26*26*26*n
        tet_table[x] += 1
        n0 = n1
        n1 = n2
        n2 = n
        if(tet_table[x] > max_value):
            max_value = tet_table[x]
            mc0 = c0
            mc1 = c1
            mc2 = c2
            mc3 = c
        c0 = c1
        c1 = c2
        c2 = c

    for i in range(0, max_table_len):
        tet_table[i] = math.log(1+tet_table[i])

def tet_table_init():
    #TODO: create tet table.
    global tet_table
    for c in tet_vals:
        i0 = alphabet.index(c[0])
        i1 = alphabet.index(c[1])
        i2 = alphabet.index(c[2])
        i3 = alphabet.index(c[3])
        n = i0 + 26 * i1 + 26 * 26 + i2 + 26 * 26 * 26 * i3
        tet_table[n] = tet_vals[c]
    print("tet_table initialized");


tet_table_init() #call necessary to initialize tet_table

def place_deciphered_text(c1, c2, iStart):
    #TODO: place deciphered characters into plain_text buff
    global plain_text
    row1 = inv_row[c1]
    col1 = inv_col[c1]
    row2 = inv_row[c2]
    col2 = inv_row[c2]
    if(row1 == row2):
        plain_text[iStart] = sq[row1][(col1+4)%5]
        plain_text[iStart + 1] = sq[row2][(col2+4)%5]
    elif(col1 == col2):
        plain_text[iStart] = sq[(row1 + 4)%5][col1]
        plain_text[iStart + 1] = sq[(row2 + 4)%5][col2]
    else:
        plain_text[iStart] = sq[row1][col2]
        plain_text[iStart + 1] = sq[row2][col1]

def decrypt():
    #TODO: put decrypted text (using place_deciphered_text) in
    global inv_row
    global inv_col
    global buff
    global sq
    global plain_text
    plain_text = [0] * buf_len
    for i in range(0, 5):
        for j in range(0, 5):
            inv_row[sq[i][j]] = i
            inv_col[sq[i][j]] = j

    for i in range(0, buf_len, 2):
        char1 = buff[i]
        char2 = buff[i+1]
        place_deciphered_text(char1, char2, i)

def calc_score(buffer_length):
    #TODO: calculate score of the resulting text
    decrypt()
    global plain_text
    score = 0.0
    for i in range(0, buf_len - 3):
        if(plain_text[i] > 25 or plain_text[i+1] > 25 or plain_text[i+2] > 25 or plain_text[i+3] > 25):
            print(str(plain_text[i]))
            print(str(plain_text[i+1]))
            print(str(plain_text[i+2]))
            print(str(plain_text[i+3]))
        n = plain_text[i] + 26*plain_text[i+1]+26*26*plain_text[i+2]+26*26*26*plain_text[i+3];
        score += tet_table[n]
    return score


def hill_climb(string):
    #TODO: actual code for hill climb
    global buf_len
    global buff
    string = string.upper()
    buf_len = 0
    for c in string:
        n = alphabet.find(c)
        if(n >= 0):
            buff.append(n)
            buf_len+=1
    #create the table
    n = 0
    for i in range(0, 5):
        for j in range(0, 5):
            sq[i][j] = n
            n+=1
            if(n == 9):
                n+=1 #skips j


    #random start
    for i in range(0, 5):
        for j in range(0, 4):
            x = randint(0, 4)
            y = randint(0,4)
            c = sq[x][y]
            sq[x][y] = sq[i][j]
            sq[i][j] = c

    #mutation
    cycle_limit = 20
    fudge_factor = 0.23
    begin_level = 1.0
    noise_step = 1.5
    noise_level = begin_level
    cycle_number = 0
    score = calc_score(buf_len)
    current_hc_score = score
    max_score = score

    print('current string')
    out_str = ""
    for i in range(0, buf_len):
        out_str += alphabet[plain_text[i]].lower()
    print(out_str)
    print('score = ' + str(score))

    mutation_count = 0
    number_accepted = 1
    for i in range(0, max_trials):
        choice = randint(0,5)
        modify_table(choice)
        score = calc_score(buf_len)
        if(score > max_score):
            max_score = score
            print('updated string')
            out_str = ""
            for i in range(0, buf_len):
                out_str += alphabet[plain_text[i]].lower()
            print(out_str)
            print('score = ' + str(score))
            key = ""
            for i in range(0, 5):
                for j in range(0, 5):
                    key+=alphabet[sq[i][j]]
            print('key = ' + key)

        #print("Current scroe = " + str(score))
        if(score > current_hc_score-fudge_factor*buf_len/(noise_level)):
            if(score != current_hc_score):
                number_accepted +=1
            current_hc_score = score
            #print('updated string')
            #out_str = ""
            #for i in range(0, buf_len):
            #    out_str += alphabet[plain_text[i]].lower()
            #print(out_str)
            #print('score = ' + str(score))
            #key = ""
            #for i in range(0, 5):
            #    for j in range(0, 5):
            #        key+=alphabet[sq[i][j]]
            #print('key = ' + key)
        else:
            modify_table(choice)
        noise_level += noise_step
        cycle_number += 1
        if(cycle_number >= cycle_limit):
            noise_level = begin_level
            cycle_number = 0
        #print(str(number_accepted))
    print('ran out of trials');

        #print if updated




def modify_table(choice):
    n1 = randint(0, 4)
    n2 = randint(0, 4)
    n3 = randint(0, 4)
    n4 = randint(0, 4)
    if(choice == 0):
        #rows are swapped
        for i in range(0, 5):
            c = sq[n1][i]
            sq[n1][i] = sq[n2][i]
            sq[n2][i] = c
    elif(choice == 1):
        #cols are swapped
        for i in range(0, 5):
            c = sq[i][n1]
            sq[i][n1] = sq[i][n2]
            sq[i][n2] = c
    elif(choice == 2):
        for i in range(0, 5):
            c = sq[i][0]
            sq[i][0] = sq[i][4]
            sq[i][4] = c
            c = sq[i][1]
            sq[i][1] = sq[i][3]
            sq[i][3] = c
    elif(choice == 3):
        for i in range(0, 5):
            c = sq[0][i]
            sq[0][i]  = sq[4][i]
            sq[4][i] = c
            c = sq[1][i]
            sq[1][i] = sq[3][i]
            sq[3][i] = c
    elif(choice == 4):
        for i in range(0, 5):
            for j in range(0, 5):
                c = sq[i][j]
                sq[i][j] = sq[j][i]
                sq[j][i] = c
    else:
        #pairs switched
        c1 = sq[n1][n2]
        sq[n1][n2] = sq[n3][n4]
        sq[n3][n4] = c1

def read_text(fileName):
    #TODO: read text from file
    ciphertext = '';
    with open(fileName, 'r') as myfile:
        ciphertext = myfile.read().replace('\n', '')
    return ciphertext

print(read_text('input.txt'))
hill_climb(read_text('input.txt'))

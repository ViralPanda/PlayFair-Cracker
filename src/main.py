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

tet_table = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
buff = [], plain_text = []
max_trials = 10000000
sq = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10,11,12,13,14],[15, 16, 17, 18, 19],[20,21,22,23,24]]
inv_row = []
inv_col = []
fudge_factor = 0.2

def create_table(string):
    #TODO: make the table using string's chars.

def tet_table_init():
    #TODO: create tet table.


tet_table_init() #call necessary to initialize tet_table

def place_deciphered_text(c1, c2, index):
    #TODO: place deciphered characters into plain_text buff

def dectrypt():
    #TODO: put decrypted text (using place_deciphered_text) in

def calc_score(buffer_length):
    #TODO: calculate score of hte resulting text

def hill_climb(string):
    #TODO: actual code for hill climb

def read_text(fileName):
    #TODO: read text from file

hill_climb(read_text('input.txt'))


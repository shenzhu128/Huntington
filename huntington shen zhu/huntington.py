import time

def progressBar(current, total, barLength = 20):
    percent = float(current + 1) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    if(current != total - 1):
        print('Current index: %d, Progress: [%s%s] %d %%' % (current, arrow, spaces, percent), end='\r')
    else:
        print('Current index: %d, Progress: [%s%s] %d %%' % (current, arrow, spaces, percent), end='\n')
    time.sleep(0.0001)

# Get the sequence of the chromosome.
f = open('chromosome.txt', 'r')
sequence = f.read()
f.close()

# Determine if the sequence is a valid sequence.
if len(sequence)%3 != 0:
    print('The length of the sequence is not correct')
    exit(1)

# First get the unique characters in the  sequence.
unique = ''.join(set(sequence))
# Sort the unique characters alphabetically.
sorted_string = ''.join(sorted(unique))
# Check if all characters are in 'ACGT', which are 4 valid nucleotides.
for i in range(len(sorted_string)):
    if(sorted_string[i] in 'ACGT'):
        continue
    else:
        print('Unexpected nucleotide:' + sorted_string[i])
        exit(1)

print('Sequence is valid. Begin Huntington\'s desease detection')

# 'hasCAGBefore' indicates whether there is a CAG trinucleotide right before the current CAG trinucleotide.
hasCAGBefore = False
# 'transitions' represents the transition function for the DFA.
transitions = {
               0: {'A':0, 'C':1, 'G':0, 'T':0},
               1: {'A':2, 'C':1, 'G':0, 'T':0},
               2: {'A':0, 'C':0, 'G':3, 'T':0},
               3: {'A':0, 'C':1, 'G':0, 'T':0}
              }
# 'state' stands for the current state, which is initially 0.
state = 0
# 'huntingtonScore'
huntingtonScore = 0
# 'indexOfLastState3'
indexOfLastState3 = -1

# Begin the transitions
# Whenever we're at the state 3, we check the index of last index of state 3.
# If current index - last index == 3, then add 1 to the huntington score
for i in range(len(sequence)):
    # Indicating the process.
    progressBar(i, len(sequence))
    state = transitions[state][sequence[i]]
    if (state == 3) & (i - indexOfLastState3 == 3):
        huntingtonScore = huntingtonScore + 1
        indexOfLastState3 = i
    elif (state == 3) & (i - indexOfLastState3 != 3):
        indexOfLastState3 = i

print('Huntington\'s score: %d' % (huntingtonScore))
if huntingtonScore >= 40:
    print('POSITIVE')
else:
    print('NEGATIVE')
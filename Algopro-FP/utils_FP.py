import random
import uuid

##### For managing the interface #####
SIZE = 540 #size of the board image
PIECE = 32 #size of the single pieces
N = 15
MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N-1)

SCORE_LONG_5 = 1000000       # Five in a row
SCORE_LIVE_4 = 100000        # Open four (live four)
SCORE_GO_4 = 10000           # One-sided four (go four)
SCORE_DEAD_4 = -10           # Blocked four
SCORE_LIVE_3 = 1000          # Open three (live three)
SCORE_SLEEP_3 = 100          # Semi-open three (sleep three)
SCORE_DEAD_3 = -10           # Blocked three
SCORE_LIVE_2 = 100           # Open two (live two)
SCORE_SLEEP_2 = 10           # Semi-open two (sleep two)
SCORE_DEAD_2 = -10           # Blocked two
SCORE_FORK = 50000           # Fork patterns

def pixel_conversion(list_points, target):
    # point of the list from where start the search
    index = int((len(list_points)-1)//2) 

    while True:
        if target < list_points[0]:
            index = 0
            break
        elif target >= list_points[-1]:
            index = len(list_points)-2
            break

        elif list_points[index] > target:
            if list_points[index-1] <= target:
                index -= 1
                break
            else:
                index -= 1

        elif list_points[index] <= target:
            if list_points[index+1] > target:
                break
            else:
                index += 1
    
    return index


# Transform pygame pixel to boardMap coordinates
def pos_pixel2map(x, y):
    start = int(MARGIN - GRID//2)
    end = int(SIZE - MARGIN + GRID//2)
    list_points = [p for p in range(start, end+1, int(GRID))]

    i = pixel_conversion(list_points, y)
    j = pixel_conversion(list_points, x)
    return (i,j)

# Transform boardMap to pygame pixel coordinates
def pos_map2pixel(i, j):
    return (MARGIN + j * GRID - PIECE/2, MARGIN + i * GRID - PIECE/2)


def create_mapping():
    pos_mapping = {}
    for i in range(N):
        for j in range(N):
            spacing = [r for r in range(MARGIN, SIZE-MARGIN+1, int(GRID))]
            pos_mapping[(i,j)] = (spacing[j],spacing[i])
    
    return pos_mapping

def add_long_5_patterns(x, patternDict):
    patternDict[(x, x, x, x, x)] = SCORE_LONG_5 * x

def add_live_4_patterns(x, patternDict):
    patterns = [
        (0, x, x, x, x, 0),
        (0, x, x, x, 0, x, 0),
        (0, x, 0, x, x, x, 0),
        (0, x, x, 0, x, x, 0)
    ]
    for p in patterns:
        patternDict[p] = SCORE_LIVE_4 * x

def add_go_4_patterns(x, patternDict):
    patterns = [
        (0, x, x, x, x, -x),
        (-x, x, x, x, x, 0)
    ]
    for p in patterns:
        patternDict[p] = SCORE_GO_4 * x

def add_dead_4_patterns(x, patternDict):
    patternDict[(-x, x, x, x, x, -x)] = SCORE_DEAD_4 * x

def add_live_3_patterns(x, patternDict):
    patterns = [
        (0, x, x, x, 0),
        (0, x, 0, x, x, 0),
        (0, x, x, 0, x, 0)
    ]
    for p in patterns:
        patternDict[p] = SCORE_LIVE_3 * x

def add_sleep_3_patterns(x, patternDict):
    patterns = [
        (0, 0, x, x, x, -x),
        (-x, x, x, x, 0, 0),
        (0, x, 0, x, x, -x),
        (-x, x, x, 0, x, 0),
        (0, x, x, 0, x, -x),
        (-x, x, 0, x, x, 0),
        (x, 0, 0, x, x),
        (x, x, 0, 0, x),
        (x, 0, x, 0, x)
    ]
    for p in patterns:
        patternDict[p] = SCORE_SLEEP_3 * x

def add_dead_3_patterns(x, patternDict):
    patternDict[(-x, x, x, x, -x)] = SCORE_DEAD_3 * x

def add_live_2_patterns(x, patternDict):
    patterns = [
        (0, 0, x, x, 0),
        (0, x, x, 0, 0),
        (0, x, 0, x, 0),
        (0, x, 0, 0, x, 0)
    ]
    for p in patterns:
        patternDict[p] = SCORE_LIVE_2 * x

def add_sleep_2_patterns(x, patternDict):
    patterns = [
        (0, 0, 0, x, x, -x),
        (-x, x, x, 0, 0, 0),
        (0, 0, x, 0, x, -x),
        (-x, x, 0, x, 0, 0),
        (0, x, 0, 0, x, -x),
        (-x, x, 0, 0, x, 0),
        (x, 0, 0, 0, x),
        (-x, 0, x, 0, x, 0, -x),
        (-x, 0, x, x, 0, 0, -x),
        (-x, 0, 0, x, x, 0, -x)
    ]
    for p in patterns:
        patternDict[p] = SCORE_SLEEP_2 * x

def add_fork_patterns(x, patternDict):
    patternDict[(0, x, x, 0, 0, x, x, 0)] = SCORE_FORK * x

#### Pattern scores ####
def create_pattern_dict(score_multiplier=1, log=False):
    patternDict = {}
    for x in [-1, 1]:  # Loop for both players
        
        add_long_5_patterns(x, patternDict)
        add_live_4_patterns(x, patternDict)
        add_go_4_patterns(x, patternDict)
        add_dead_4_patterns(x, patternDict)
        add_live_3_patterns(x, patternDict)
        add_sleep_3_patterns(x, patternDict)
        add_dead_3_patterns(x, patternDict)
        add_live_2_patterns(x, patternDict)
        add_sleep_2_patterns(x, patternDict)
        add_fork_patterns(x, patternDict)

        for key in patternDict:
            patternDict[key] *= score_multiplier

         # Log patterns for debugging if requested
        if log:
            for pattern, score in patternDict.items():
                print(f"Pattern: {pattern}, Score: {score}")

        # long_5
        patternDict[(x, x, x, x, x)] = SCORE_LONG_5 * x

        # live_4
        patternDict[(0, x, x, x, x, 0)] = SCORE_LIVE_4 * x
        patternDict[(0, x, x, x, 0, x, 0)] = SCORE_LIVE_4 * x
        patternDict[(0, x, 0, x, x, x, 0)] = SCORE_LIVE_4 * x
        patternDict[(0, x, x, 0, x, x, 0)] = SCORE_LIVE_4 * x

        # go_4
        patternDict[(0, x, x, x, x, -x)] = SCORE_GO_4 * x
        patternDict[(-x, x, x, x, x, 0)] = SCORE_GO_4 * x

        # dead_4
        patternDict[(-x, x, x, x, x, -x)] = SCORE_DEAD_4 * x

        # live_3
        patternDict[(0, x, x, x, 0)] = SCORE_LIVE_3 * x
        patternDict[(0, x, 0, x, x, 0)] = SCORE_LIVE_3 * x
        patternDict[(0, x, x, 0, x, 0)] = SCORE_LIVE_3 * x

        # sleep_3
        patternDict[(0, 0, x, x, x, -x)] = SCORE_SLEEP_3 * x
        patternDict[(-x, x, x, x, 0, 0)] = SCORE_SLEEP_3 * x
        patternDict[(0, x, 0, x, x, -x)] = SCORE_SLEEP_3 * x
        patternDict[(-x, x, x, 0, x, 0)] = SCORE_SLEEP_3 * x
        patternDict[(0, x, x, 0, x, -x)] = SCORE_SLEEP_3 * x
        patternDict[(-x, x, 0, x, x, 0)] = SCORE_SLEEP_3 * x
        patternDict[(x, 0, 0, x, x)] = SCORE_SLEEP_3 * x
        patternDict[(x, x, 0, 0, x)] = SCORE_SLEEP_3 * x
        patternDict[(x, 0, x, 0, x)] = SCORE_SLEEP_3 * x
        patternDict[(-x, 0, x, x, x, 0, -x)] = SCORE_SLEEP_3 * x

        # dead_3
        patternDict[(-x, x, x, x, -x)] = SCORE_DEAD_3 * x

        # live_2
        patternDict[(0, 0, x, x, 0)] = SCORE_LIVE_2 * x
        patternDict[(0, x, x, 0, 0)] = SCORE_LIVE_2 * x
        patternDict[(0, x, 0, x, 0)] = SCORE_LIVE_2 * x
        patternDict[(0, x, 0, 0, x, 0)] = SCORE_LIVE_2 * x

        # sleep_2
        patternDict[(0, 0, 0, x, x, -x)] = SCORE_SLEEP_2 * x
        patternDict[(-x, x, x, 0, 0, 0)] = SCORE_SLEEP_2 * x
        patternDict[(0, 0, x, 0, x, -x)] = SCORE_SLEEP_2 * x
        patternDict[(-x, x, 0, x, 0, 0)] = SCORE_SLEEP_2 * x
        patternDict[(0, x, 0, 0, x, -x)] = SCORE_SLEEP_2 * x
        patternDict[(-x, x, 0, 0, x, 0)] = SCORE_SLEEP_2 * x
        patternDict[(x, 0, 0, 0, x)] = SCORE_SLEEP_2 * x
        patternDict[(-x, 0, x, 0, x, 0, -x)] = SCORE_SLEEP_2 * x
        patternDict[(-x, 0, x, x, 0, 0, -x)] = SCORE_SLEEP_2 * x
        patternDict[(-x, 0, 0, x, x, 0, -x)] = SCORE_SLEEP_2 * x

        # dead_2
        patternDict[(-x, x, x, -x)] = SCORE_DEAD_2 * x

    return patternDict



##### Zobrist Hashing #####
def init_zobrist():
    zTable = [[[uuid.uuid4().int  for _ in range(2)] \
                        for j in range(15)] for i in range(15)] #changed to 32 from 64
    return zTable

def update_TTable(table, hash, score, depth):
    table[hash] = [score, depth]
from AI import *
import math
import time
from copy import deepcopy
import pandas as pd
import os
import matplotlib.pyplot as plt

# Example of configurable moves list (could be passed as an argument)
moves_list = [
    (7, 7), (8, 8), (8, 6), (6, 8),
    (7, 8), (7, 9), (7, 5), (9, 7),
    (7, 6), (7, 4), (10, 6), (9, 6),
    (9, 5), (8, 5), (10, 7), (8, 10)
]

# Initialize GomokuAI object in order to create a board
AI = GomokuAI()


def board_to_eval(ai, moves):
    ai.currentState = 1  # AI starts first (CAN be changed)
    board_value = 0

    for m in moves:
        turn = ai.currentState

        ai.boardValue = ai.evaluate(m[0], m[1], board_value, -1, ai.nextBound)
        ai.setState(m[0], m[1], turn)
        ai.currentI, ai.currentJ = m[0], m[1]
        ai.updateBound(m[0], m[1], ai.nextBound)
        ai.emptyCells -= 1
        ai.currentState *= -1


def ai_runtime(ai, depth_range=range(1, 7)):
    board_to_eval(ai, moves_list)
    runtime = []
    moves_chosen = []

    for i in depth_range:
        new_ai = deepcopy(ai)
        start_time = time.time()
        new_ai.alphaBetaPruning(i, new_ai.boardValue, new_ai.nextBound, -math.inf, math.inf, True)
        end_time = time.time()
        time_diff = end_time - start_time
        runtime.append(time_diff)

        moves_chosen.append((new_ai.currentI, new_ai.currentJ))
        print(f"Done depth {i} in {time_diff:.4f} seconds")

    return runtime, moves_chosen


def save_results(runtime, moves_chosen, filename='performance_eval.csv'):
    # Check if the file exists to decide whether to append or create a new file
    file_exists = os.path.exists(filename)
    df = pd.DataFrame({'runtime': runtime, 'moves_chosen': moves_chosen})
    
    if file_exists:
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)


def plot_runtime(runtime, depths):
    plt.plot(depths, runtime, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    plt.xlabel('Search Depth', fontsize=14)
    plt.ylabel('Time (seconds)', fontsize=14)
    plt.title('AI Runtime vs Search Depth', fontsize=16)
    plt.grid(True)
    plt.xticks(depths)
    plt.show()


if __name__ == '__main__':
    # Define depth range as an argument
    depth_range = range(1, 7)
    
    runtime, moves_chosen = ai_runtime(AI, depth_range)
    
    # Save results to CSV
    save_results(runtime, moves_chosen, filename='performance_eval.csv')

    # Print runtime and moves chosen for debugging/inspection
    print("Runtime:", runtime)
    print("Moves Chosen:", moves_chosen)

    # Plot runtime vs. depth
    plot_runtime(runtime, list(depth_range))

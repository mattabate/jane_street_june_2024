import time
import random

SIZE = 5
import json

import random

import tqdm


t0 = time.time()

SAVE_FILE = f"results/bests_{int(t0)}.json"

with open("states.json") as f:
    data = json.load(f)


states_i_care_about = [
    "CALIFORNIA",
    "ARIZONA",
    "TEXAS",
    "LOUISIANA",
    "MISSISSIPPI",
    "ALABAMA",
    "FLORIDA",
]


states_i_care_about = [
    "PENNSYLVANIA",
]

unique_letters = set()
for s in states_i_care_about:
    for c in s:
        unique_letters.add(c)
unique_letters = list(unique_letters)
print(
    unique_letters
)  # ['U', 'D', 'L', 'F', 'X', 'B', 'R', 'M', 'O', 'S', 'E', 'I', 'T', 'P', 'A', 'N', 'C', 'Z']

# letters i dont care about
# [G, H, J, K, Q, V, W, Y]

grid: list[str] = [
    "VMHWA",
    "LCISQ",
    "NOANG",
    "TIROF",
    "REGLI",
]
# grid = ["".join(random.sample(unique_letters, SIZE)) for _ in range(SIZE)]
# # mix up letters to make grid

flips = 4

bests = []

annealing_time = 50000
start_flips = 10
end_flips = 1


def get_kings_moves(pos: tuple[int, int]) -> list[tuple[int, int]]:
    moves = []
    for i in range(-1, 2):
        x = pos[0] + i
        for j in range(-1, 2):
            y = pos[1] + j
            if i == 0 and j == 0:
                continue
            if 0 <= x < SIZE and 0 <= y < SIZE:
                moves.append((x, y))

    return moves


def iterate(index, starting: list[tuple[int, int]], grid: list[str], word: str):
    surviving = []
    for s in starting:
        km = get_kings_moves(s)
        for move in km:
            if grid[move[0]][move[1]] == word[index]:
                surviving.append(move)

    return surviving


def word_possible_at_point(start: tuple[int, int], grid: list[str], word: str):
    current_letter = grid[start[0]][start[1]]
    extra_life = True

    if current_letter == word[0]:
        starting = [start]
    elif current_letter != word[0]:
        extra_life = False
        starting = get_kings_moves(start)

    for i in range(1, len(word)):
        new_starting = iterate(i, starting, grid, word)
        if not new_starting:
            if extra_life:
                extra_life = False
                new_starting = []
                for s in starting:
                    new_starting += get_kings_moves(s)
            else:
                return False
        starting = new_starting
    else:
        return True


def process(grid: list[str]) -> tuple[int, list[str]]:
    score = 0
    states = []
    for state, population in data:
        possible = False
        for i in range(SIZE):
            for j in range(SIZE):
                if word_possible_at_point((i, j), grid, state):
                    possible = True
                    score += population
                    states.append(state)

                    break
            if possible:
                break
    return score, states


cutoff = 165379868
score, _ = process(grid)
print("final score:", score, score > cutoff, (score - cutoff) / cutoff * 100, "%")


def random_flip(grid: list[str]) -> list[str]:
    new_grid = grid.copy()
    x = random.randint(0, SIZE - 1)
    y = random.randint(0, SIZE - 1)
    new_grid[x] = new_grid[x][:y] + chr(random.randint(65, 90)) + new_grid[x][y + 1 :]
    return new_grid


best_score = score
best_grid = grid.copy()


score, states = process(grid)
print("------------------")
print(json.dumps(best_grid, indent=4))
print(states)
print("initial score:", "\033[93m", best_score, "\033[0m")

score, states = process(grid)


t0 = time.time()
while True:
    for tries in tqdm.tqdm(range(annealing_time)):
        new_grid = best_grid.copy()
        for i in range(flips):
            new_grid = random_flip(new_grid)

        score, states = process(new_grid)
        if score > best_score:
            best_score = score
            best_grid = new_grid
            print()
            print("------------------")
            print(json.dumps(best_grid, indent=4))
            print(states)
            print("new best score:", "\033[93m", best_score, "\033[0m")

            bests.append((best_score, len(states), best_grid, states))
            with open(SAVE_FILE, "w") as f:
                json.dump(bests, f, indent=4)
            break

        # flips == 25 when tries = 0 and flips = 2 when tries = annealing_time
        flips = int(start_flips - (tries / annealing_time) * (start_flips - end_flips))
        if tries > annealing_time:
            break
    else:
        break

print("fin", "time:", time.time() - t0, "seconds")

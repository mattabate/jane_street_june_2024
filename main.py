SIZE = 3


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


def somehting(index, starting: list[tuple[int, int]], grid: list[str], word: str):
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
        new_starting = somehting(i, starting, grid, word)
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


grid: list[str] = ["THO", "AIN", "ESL"]


import json

with open("states.json") as f:
    STATES = json.load(f)

for state in STATES:
    possible = False
    for i in range(SIZE):
        for j in range(SIZE):
            if word_possible_at_point((i, j), grid, state):
                possible = True
                print(state, possible, (i, j))
                break
        if possible:
            break

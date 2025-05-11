"""
pytest fuzz-suite for lc909-bfs-with-dominance-proof.

Run with:
    python -m pytest -q
Typical runtime: ~3 s on CPython 3.12.
"""

import random
from collections import deque

import pytest

from solution import Solution


# ---------- helper: naive BFS (no edge reduction) ----------
def naive_bfs(board):
    n = len(board)
    cells = [-1]
    ltr = True
    for r in range(n - 1, -1, -1):
        row = board[r] if ltr else reversed(board[r])
        cells.extend(row)
        ltr = not ltr
    target = len(cells) - 1

    q = deque([(1, 0)])
    seen = {1}
    while q:
        sq, d = q.popleft()
        if sq == target:
            return d
        for r in range(1, 7):
            nxt = sq + r
            if nxt > target:
                continue
            if cells[nxt] != -1:
                nxt = cells[nxt]
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, d + 1))
    return -1


# ---------- deterministic unit test (LC sample) ----------
def test_sample_board():
    board = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1],
    ]
    assert Solution().snakesAndLadders(board) == 4


# ---------- fuzz suite ----------
@pytest.mark.parametrize("seed", range(200))  # 200 seeds ≈ 3 s total
def test_random_board(seed):
    random.seed(seed)

    # board size: 4 × 4 to 10 × 10  (up to 100 squares)
    n = random.randint(4, 10)
    size = n * n

    # start with all -1
    flat = [-1] * (size + 1)

    # randomly sprinkle snakes/ladders (≤ 10% of squares, never 1 or target)
    for _ in range(size // 10):
        src = random.randint(2, size - 1)
        dst = random.randint(2, size - 1)
        if dst == src:
            continue
        flat[src] = dst

    # un-flatten into LC’s zig-zag pattern
    board = []
    idx = 1
    for row in range(n):
        level = []
        for _ in range(n):
            level.append(flat[idx])
            idx += 1
        if row % 2 == 1:
            level.reverse()
        board.insert(0, level)  # LC builds from bottom up

    sol = Solution().snakesAndLadders(board)
    ref = naive_bfs(board)
    assert sol == ref, f"Seed {seed} failed: sol={sol}, ref={ref}"

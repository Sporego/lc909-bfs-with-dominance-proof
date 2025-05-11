"""
demo.py  –  Quick manual run against LeetCode 909’s sample board.

$ python demo.py
Minimal rolls required: 4
"""

from solution import Solution

# LC 909 sample board
# (-1 = plain square, otherwise destination of a snake/ladder)
sample_board = [
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, 35, -1, -1, 13, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, 15, -1, -1, -1, -1],
]

moves = Solution().snakesAndLadders(sample_board)
print(f"Minimal rolls required: {moves}")

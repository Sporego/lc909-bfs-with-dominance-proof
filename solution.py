from collections import deque
from typing import List

class Solution:
    """
    BFS with 'deepest ordinary square' edge–reduction
    for LeetCode 909 (Snakes & Ladders).

    • Always enqueue every ladder/snake jump reachable
      by rolls 1-6.

    • Among the remaining plain landings enqueue only
      the deepest one, marking the others visited so
      they are never reconsidered.

    This halves–to–quarter the queue size in practice
    while preserving the minimal-move guarantee.
    """

    def snakesAndLadders(self, board: List[List[int]]) -> int:
        # ---------- 1. Flatten zig-zag board ---------- #
        n_rows = len(board)
        cells: List[int] = [-1]                 # cells[1] = square 1
        left_to_right = True
        for r in range(n_rows - 1, -1, -1):     # bottom → top
            row = board[r] if left_to_right else reversed(board[r])
            cells.extend(row)
            left_to_right = not left_to_right
        target = len(cells) - 1                 # final square number

        # ---------- 2. BFS initialisation ---------- #
        queue   = deque([(1, 0)])               # (square, moves)
        visited = {1}

        # ---------- 3. Main loop ---------- #
        while queue:
            square, moves = queue.popleft()

            # One roll can finish from here?
            if square >= target - 6:
                return moves + 1

            # Which rolls land on a jump?
            jump_mask = [cells[square + r] != -1 for r in range(1, 7)]

            deepest_plain = None
            for r in range(6, 0, -1):           # rolls 6 → 1
                landing = square + r
                if landing > target:
                    continue

                if jump_mask[r - 1]:            # ladder / snake
                    dest = cells[landing]
                    if dest == target:          # jump reaches goal
                        return moves + 1
                    if dest not in visited:
                        visited.add(dest)
                        queue.append((dest, moves + 1))
                else:                           # ordinary landing
                    if landing not in visited:
                        visited.add(landing)    # mark now
                        if deepest_plain is None:
                            deepest_plain = landing  # keep only one

            if deepest_plain is not None:       # enqueue deepest plain
                queue.append((deepest_plain, moves + 1))

        return -1                               # unreachable

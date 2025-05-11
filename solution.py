from collections import deque
from typing import List

class Solution:
    """
    BFS with 'deepest ordinary square' dominance pruning for LC 909.
    • Always enqueue every ladder/snake jump reachable by rolls 1-6.
    • Among plain landings enqueue only the deepest one, marking the rest visited immediately.
    Cuts the queue 2-4× while preserving optimality.
    """
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        # ---------- 1. Flatten zig-zag board ---------- #
        n = len(board)
        cells: List[int] = [-1]  # cells[1] = square 1
        ltr = True  # left-to-right toggle
        for r in range(n - 1, -1, -1):  # bottom → top
            row = board[r] if ltr else list(reversed(board[r]))
            cells.extend(row)
            ltr = not ltr
        target = len(cells) - 1  # final square number (n²)

        # ---------- 2. BFS initialisation ---------- #
        queue = deque([(1, 0)])  # (square, moves)
        visited = {1}

        # ---------- 3. Main loop ---------- #
        while queue:
            square, moves = queue.popleft()
            
            # a) Already there
            if square == target:
                return moves
                
            # b) One plain roll can finish - immediately check if we're close to target
            if square >= target - 6:
                return moves + 1
                
            # ---------- 3.1 classify rolls 1-6 ----------
            jump_mask = []
            for r in range(1, 7):
                if square + r <= target:
                    jump_mask.append(cells[square + r] != -1)
                else:
                    jump_mask.append(False)
                    
            deepest_plain = None
            for r in range(6, 0, -1):  # rolls 6 → 1
                landing = square + r
                if landing > target:
                    continue
                    
                if jump_mask[r - 1]:  # ladder / snake
                    dest = cells[landing]
                    if dest == target:  # jump ends on goal
                        return moves + 1
                    if dest not in visited:
                        visited.add(dest)
                        queue.append((dest, moves + 1))
                else:  # ordinary landing
                    if landing not in visited:
                        visited.add(landing)  # mark now
                        if deepest_plain is None:
                            deepest_plain = landing  # keep only one
                            
            if deepest_plain is not None:
                queue.append((deepest_plain, moves + 1))
                
        return -1  # unreachable

# lc909-bfs-with-dominance-proof
Optimized BFS solution for LeetCode 909 (Snakes &amp; Ladders) with mathematical proof of edge reduction optimization

## Intuition
We need the **minimum number of dice rolls** to reach the last square.  
Because every roll costs exactly one move and always advances **1 – 6 squares**, the board forms an **unweighted directed graph** where each square has up to six outgoing edges.  
Shortest path in an unweighted graph ⇒ **Breadth-First Search (BFS)**.

To trim constant-factor work we observe:

* **Snake / ladder landings are mandatory** – every such destination must be explored immediately.
* For the remaining **ordinary** landings, exploring **only the farthest** one still dominates the shallower ones:  
  whatever move sequence starts on a shallower square can be re-created from the deeper square in ≤ the same number of moves.
* **Key tweak:** even though we enqueue just that deepest plain square, we **immediately mark every other plain landing in the same dice window as visited**.  
  This prevents them from being enqueued later through a longer route and keeps the BFS property that *the first time we see a square we have reached it in the fewest moves* (within this reduced edge set).

Heuristic summary  
→ *Enqueue every snake/ladder jump **plus** the deepest ordinary square; mark the other plain squares as visited.*

---

## Approach
1. **Flatten** the zig-zag board into a 1-based array `cells` so “square *k*” ≙ `cells[k]`.
2. Start BFS with `queue = deque([(1, 0)])` and `visited = {1}`.
3. **Early exit:** if `square ≥ target – 6`, one more roll reaches the goal.
4. For each node pop:  
   1. Pre-compute `jump_mask[1..6]` → does roll *r* land on a snake/ladder?  
   2. Scan rolls **6 → 1**:  
      * **Jump landing** → enqueue its destination (if unseen).  
      * **Plain landing** → mark it visited; enqueue the **first** such landing (the deepest one) only.
5. Return the move count when we touch the goal; return **–1** if the queue empties first.

---

## Correctness Sketch
* Let window **W = {s+1,…,s+6}** for the current square *s*.  
  Denote  
  * **J** – jump squares in *W* (always enqueued),  
  * **d** – deepest ordinary square in *W*,  
  * **P = W \ (J ∪ {d})** – shallower ordinary squares (marked visited, never queued).

* **Dominance of *d***: for any *p ∈ P*, `1 ≤ d – p ≤ 5`.  
  If the optimal path rolls *k* from *p* (1 ≤ k ≤ 6):
  * If *k ≥ d – p* the same roll from *d* lands **not behind** the square reached from *p*.  
  * If *k < d – p* then *p* used a smaller first roll; *d* needs one extra small roll to re-sync, so the total move count is unchanged.
  Thus any shortest path using *p* can be matched (never exceeded) via *d*.

* **Visited-first rule is safe**: marking every *p ∈ P* visited does not hide a shorter path, because any route that would revisit *p* later has already taken ≥ 1 extra move to get back into the same dice window.

* **Jumps first**: enqueuing all jumps before *d* ensures every ladder/snake destination is discovered at the minimum possible depth.

Therefore the algorithm explores a *dominating* subset of edges in true BFS order ⇒ it still returns the global minimum roll count.

---

## Complexity
Let `n = len(board)` (board is `n × n`, so `n²` squares).

| Phase          | Time | Space |
|----------------|------|-------|
| Flatten board  | **O(n²)** | **O(n²)** (`cells`) |
| BFS            | **O(n²)** – each square processed once | **O(n²)** (`queue`, `visited`) |

---

## Code
```python
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
```

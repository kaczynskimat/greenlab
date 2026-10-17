# modified_dfs.py (G19: in_bounds inlinet)
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()

        islands = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visited:
                    islands += 1
                    stack = [(r, c)]
                    visited.add((r, c))

                    while stack:
                        row, col = stack.pop()
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                stack.append((nr, nc))

        return islands
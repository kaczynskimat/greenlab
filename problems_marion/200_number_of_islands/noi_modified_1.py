from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        islands = 0
        visited = set()
        rows, cols = len(grid), len(grid[0])

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visited:
                    islands += 1
                    q = deque()
                    visited.add((r, c))
                    q.append((r, c))

                    while q:
                        row, col = q.popleft()
                        directions = [[1,0],[-1,0],[0,1],[0,-1]]

                        for dr, dc in directions:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in visited:
                                q.append((nr, nc))
                                visited.add((nr, nc))

        return islands
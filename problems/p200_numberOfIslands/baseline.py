from collections import deque
from typing import List
# -----------------------------------------------
# Variation 1:
# -----------------------------------------------
class SolutionV1:
    def numIslands(self, grid: List[List[str]]) -> int:
        islands = 0
        visited = set()
        rows, cols = len(grid), len(grid[0])
        def bfs(r, c):
            q = deque()
            visited.add((r, c))
            q.append((r, c))
            while q:
                row, col = q.popleft()
                directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == "1"
                        and (nr, nc) not in visited
                    ):
                        q.append((nr, nc))
                        visited.add((nr, nc))
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visited:
                    islands += 1
                    bfs(r, c)
        return islands
# -----------------------------------------------
# Variation 2:
# -----------------------------------------------
class SolutionV2:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()
        def in_bounds(r, c):
            return 0 <= r < rows and 0 <= c < cols
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
                            if (
                                in_bounds(nr, nc)
                                and grid[nr][nc] == "1"
                                and (nr, nc) not in visited
                            ):
                                visited.add((nr, nc))
                                stack.append((nr, nc))
        return islands
# -----------------------------------------------
# Variation 3:
# -----------------------------------------------
class SolutionV3:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        parent = list(range(rows * cols))
        def in_bounds(r, c):
            return 0 <= r < rows and 0 <= c < cols
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    count += 1
                    for dr, dc in ((1, 0), (0, 1)):
                        nr, nc = r + dr, c + dc
                        if in_bounds(nr, nc) and grid[nr][nc] == "1":
                            root_a = find(r * cols + c)
                            root_b = find(nr * cols + nc)
                            if root_a != root_b:
                                parent[root_a] = root_b
                                count -= 1
        return count
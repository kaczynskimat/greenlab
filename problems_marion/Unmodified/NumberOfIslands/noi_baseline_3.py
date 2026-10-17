from typing import List


class Solution:
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
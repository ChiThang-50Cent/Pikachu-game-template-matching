from collections import deque
import numpy as np

def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque()
    visited = set()
    parent = {}

    queue.append(start)
    visited.add(start)
    parent[start] = None

    while queue:
        current = queue.popleft()

        if current == end:
            # Đã tìm thấy đích, bạn có thể truy ngược lại từ end sử dụng parent
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        row, col = current
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

        for neighbor in neighbors:
            n_row, n_col = neighbor            
            if (0 <= n_row < rows and 0 <= n_col < cols) and ((maze[n_row][n_col] == 0 and neighbor not in visited) or neighbor == end): 
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return None  # Không tìm thấy đường đi

# Mảng đã cung cấp
maze_array = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 14, 17, 18, 0, 0, 0, 5, 0, 0, 21, 2, 1, 16, 7, 26, 0],
    [0, 30, 18, 16, 24, 4, 3, 6, 34, 28, 19, 10, 32, 11, 4, 17, 7, 0],
    [0, 25, 24, 13, 29, 12, 27, 13, 28, 5, 29, 12, 20, 33, 12, 0, 0, 0],
    [0, 16, 18, 34, 14, 26, 31, 16, 3, 28, 0, 5, 10, 23, 9, 0, 0, 0],
    [0, 23, 3, 17, 36, 5, 27, 11, 19, 36, 0, 8, 6, 18, 14, 28, 10, 0],
    [0, 2, 0, 0, 31, 35, 20, 14, 13, 15, 33, 7, 0, 3, 21, 29, 22, 0],
    [0, 8, 0, 0, 0, 0, 15, 2, 29, 27, 8, 21, 0, 32, 0, 0, 25, 0],
    [0, 30, 15, 22, 24, 7, 1, 23, 12, 33, 26, 34, 8, 11, 13, 35, 33, 0],
    [0, 17, 31, 10, 34, 24, 0, 27, 26, 21, 2, 9, 31, 15, 0, 23, 11, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start_point = (2, 6)
end_point = (5, 2)

# print(np.array(maze_array))

result = bfs(maze_array, start_point, end_point)

if result:
    print(f"Đường đi từ {start_point} đến {end_point}: {result}")
else:
    print(f"Không có đường đi từ {start_point} đến {end_point}.")
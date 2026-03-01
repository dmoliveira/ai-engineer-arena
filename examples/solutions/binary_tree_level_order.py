from collections import deque


def solve(values):
    if not values:
        return []

    levels = []
    queue = deque([(0, 0)])

    while queue:
        index, depth = queue.popleft()
        if index >= len(values):
            continue
        value = values[index]
        if value is None:
            continue

        if depth == len(levels):
            levels.append([])
        levels[depth].append(value)

        queue.append((2 * index + 1, depth + 1))
        queue.append((2 * index + 2, depth + 1))

    return levels

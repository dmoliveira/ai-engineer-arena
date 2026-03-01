def solve(intervals):
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda item: item[0])
    merged = [intervals[0][:]]

    for start, end in intervals[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return merged

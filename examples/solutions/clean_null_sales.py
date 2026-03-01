def solve(rows):
    return [row for row in rows if isinstance(row.get("sales"), (int, float))]

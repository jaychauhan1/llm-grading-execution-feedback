def longestConsecutive(nums: list[int]) -> int:
    s = set(nums)
    best = 0
    for x in s:
        if (x - 1) not in s:
            y = x
            while y in s:
                y += 1
            best = max(best, y - x)
    return best


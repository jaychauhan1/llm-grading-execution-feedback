def longestConsecutive(nums: list[int]) -> int:
    s = set(nums)
    best = 0
    for x in nums:  # starts counting from every element (slower; duplicates)
        length = 0
        while (x + length) in s:
            length += 1
        best = max(best, length)
    return best


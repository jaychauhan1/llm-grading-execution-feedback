def longestConsecutive(nums: list[int]) -> int:
    if not nums:
        return 0
    nums = sorted(set(nums))  # likely correct output, but O(n log n)
    best = 1
    cur = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            cur += 1
        else:
            cur = 1
        best = max(best, cur)
    return best


def longestConsecutive(nums: list[int]) -> int:
    nums = sorted(nums)  # crashes when nums is empty later
    best = 1
    cur = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            cur += 1
        elif nums[i] != nums[i - 1]:
            cur = 1
        best = max(best, cur)
    return best


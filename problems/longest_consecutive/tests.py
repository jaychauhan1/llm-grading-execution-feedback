import random
from problems.longest_consecutive.reference import longestConsecutive as ref
def gen_tests():
    tests = []

    # Basic examples
    tests.append(([100, 4, 200, 1, 3, 2], 4))
    tests.append(([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9))

    # Edge cases
    tests.append(([], 0))
    tests.append(([1], 1))
    tests.append(([1, 1, 1], 1))
    tests.append(([1, 2, 0, 1], 3))
    tests.append(([-1, -2, -3, 10], 3))

    # Randomized tests with oracle (deterministic seed)
    rnd = random.Random(1337)
    for _ in range(20):
        n = rnd.randint(0, 50)
        arr = [rnd.randint(-20, 20) for _ in range(n)]
        tests.append((arr, ref(arr)))

    return tests


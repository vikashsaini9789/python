from collections import Counter

arr = [1, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 3, 2, 5, 3, 3, 5]

count = Counter(arr)

repeats = [item for item in count.items() if item[1] > 1]

repeats.sort(key=lambda x: -x[1])

for i in range(min(3, len(repeats))):
    print(f"{i + 1}st most repeating number : {repeats[i][0]} ({repeats[i][1]} times)")
# Sorting Algorithms

Three small Python programs that sort numbers you type in. Each one reads the same way, then sorts with a different method so you can watch the difference.

## How to run

1. Run one of the `.py` files with Python.
2. Type a number and press Enter. Decimals and negative numbers are allowed.
3. Repeat until the list is complete.
4. Type `end` to start the sort.

Anything that is not a number is skipped, and the program asks again. Every value is stored as a decimal, so `2` is kept as `2.0`.

```text
3
1
3
end
```

## The programs

| Program | Method | What it prints |
| --- | --- | --- |
| `bubble_sort.py` | Compare neighbours and move the smaller one forward. A pass with no swaps means the list is sorted. | The list after every pass, then a one-second pause. |
| `bogo_sort.py` | Shuffle the whole list at random until it happens to be in order. | Every shuffle, then how many tries it took. |
| `random_quick_sort.py` | Pick a random pivot, put smaller values on the left and the rest on the right, then sort those sides the same way. A pair of values is compared directly. | Only the finished list. |

Bubble sort and quick sort always finish. Bogo sort finishes quickly on a very short list and can take a long time on a longer one, because it is just guessing. An empty list, from typing `end` immediately, comes back at once with 0 tries.

Equal values stay in order: a move or a new shuffle only happens when a value is strictly greater than the one after it. In the quick sort, a value equal to the pivot goes to the right.

## How each one works

### Bubble sort

Bubble sort walks along the list and compares each number with the one after it.

Take `[3, 1, 4]`.

1. `3` is greater than `1`, so `1` is moved in front. The list is now `[1, 3, 4]`.
2. `3` is smaller than `4`, so those two stay put.
3. The last number has nothing after it, so the pass ends.

The program then prints the list and waits one second. If that pass never had to move a number, every neighbour is already in order and the sort stops. If it did move something, it starts another pass from the beginning.

`[3, 1, 3]` needs more than one pass. The first pass turns it into `[1, 3, 3]`, and the second pass finds nothing to move.

### Bogo sort

Bogo sort does not look for a smart swap. It shuffles the whole list, then checks it.

After each shuffle it looks at every pair of neighbours. If a number is greater than the one after it, that shuffle is not sorted. If every neighbour pair is in order, the list is done and the program prints how many shuffles it used.

`[3, 1, 2]` might become `[2, 3, 1]` (still mixed), then `[1, 2, 3]` (done). A one-number list is already sorted after a single check. An empty list is returned before any shuffle.

There is no pattern to the shuffles, so a longer list can take many tries.

### Random quick sort

Quick sort splits the list around one chosen value, called the pivot, and sorts the two sides separately.

For three or more numbers the program does this:

1. Pick a pivot at random and lift it out of the list.
2. Put every smaller number on the left.
3. Put every equal or larger number on the right.
4. Sort both sides the same way, then place the pivot between them.

Two numbers skip the pivot. They are placed in order with one comparison. One number, or an empty side, is already finished.

The sides come back nested. A final step flattens them into one list: everything from the left, then the pivot, then everything from the right.

Suppose the list is `[3, 1, 4, 2]` and the pivot happens to be `3`.

- Left: `[1, 2]`
- Pivot: `3`
- Right: `[4]`

`[1, 2]` is a pair, so it becomes `1` then `2`. `[4]` stays as it is. Flattening joins those pieces into `[1, 2, 3, 4]`.

The pivot is random, so the same list can be split differently on another run. The final order is the same.

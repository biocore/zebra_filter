class IndexRange:
    __slots__ = ['start', 'end']

    # start and end are both inclusive.
    # IndexRange(1,1) is length 1
    # IndexRange(1,0) is invalid
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return str((self.start, self.end))

    def __len__(self):
        return self.end - self.start + 1


class SortedRangeList:
    def __init__(self):
        self.ranges = []

    def add_range(self, range):
        self.ranges.append(range)

    def compress(self):
        # Sort ranges by start index
        self.ranges.sort(key=lambda r: r.start)

        new_ranges = []
        start_val = None
        end_val = None

        for r in self.ranges:
            if end_val is None:
                # case 1: no active range, start active range.
                start_val = r.start
                end_val = r.end
            elif end_val >= r.start - 1:
                # case 2: active range continues through this range
                # extend active range
                end_val = max(end_val, r.end)
            else:  # if end_val < range.start - 1:
                # case 3: active range ends before this range begins
                # write new range out, then start new active range
                new_range = IndexRange(start_val, end_val)
                new_ranges.append(new_range)
                start_val = r.start
                end_val = r.end

        if end_val is not None:
            new_range = IndexRange(start_val, end_val)
            new_ranges.append(new_range)

        self.ranges = new_ranges

    def compute_length(self):
        total = 0
        for r in self.ranges:
            total += len(r)
        return total

    def __str__(self):
        return str(self.ranges)

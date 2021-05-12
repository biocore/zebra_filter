class RangeNode:
    def __init__(self, val, is_start):
        self.val = val
        self.is_start = is_start
        self.other = None

    def length(self):
        if self.is_start:
            return self.other.val - self.val + 1
        else:
            return self.val - self.other.val + 1


class IndexRange:
    # start_val and end_val are both inclusive.
    # IndexRange(1,1) is length 1
    # IndexRange(1,0) is invalid
    def __init__(self, start_val, end_val):
        self.start = RangeNode(start_val, True)
        self.end = RangeNode(end_val, False)
        self.start.other = self.end
        self.end.other = self.start


class SortedRangeList:
    def __init__(self):
        self.nodes = []

    def add_range(self, range):
        if range.end.val < range.start.val:
            return
        self.nodes.append(range.start)

    def compress(self):
        # We sort such that start nodes come before end nodes of the same value
        self.nodes.sort(key=lambda x: x.val * 2 - x.is_start)

        new_nodes = []
        start_val = None
        end_val = None

        for node in self.nodes:
            if end_val is None:
                # case 1: no active node, start active node.
                start_val = node.val
                end_val = node.other.val
            elif end_val >= node.val - 1:
                # case 2: active node continues through this range
                # extend active range
                end_val = max(end_val, node.other.val)
            else:  # if end_val < node.val - 1:
                # case 3: active node ends before this range begins
                # write new node out, then start new active node
                new_range = IndexRange(start_val, end_val)
                new_nodes.append(new_range.start)
                start_val = node.val
                end_val = node.other.val

        if end_val is not None:
            new_range = IndexRange(start_val, end_val)
            new_nodes.append(new_range.start)

        self.nodes = new_nodes

    def compute_length(self):
        total = 0
        for node in self.nodes:
            total += node.length()
        return total

    def __str__(self):
        pairs = [(node.val, node.other.val) for node in self.nodes]
        return str(pairs)

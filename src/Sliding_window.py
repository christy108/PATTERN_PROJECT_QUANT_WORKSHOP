# TODO: Change start index logic!
class Sliding_window:
    def __init__(self, direction_list, length_of_window, index_of_window):
        self.direction_list = direction_list
        self.length_of_window = length_of_window
        self.index_of_window = index_of_window
        self.increments = []
        self.set_increments()

    def set_increments(self):
        for i in range(self.length_of_window):
            i += self.index_of_window
            if i >= len(self.direction_list):
                break
            self.increments.append(self.direction_list[i])

    def get_increments(self):
        return self.increments

    def get_increments_at_index(self, index):
        return self.increments[index]

    def get_start_indices(self):
        """Return range of valid start indices for sliding over all positions (0 .. len - length_of_window)."""
        n = len(self.direction_list)
        return range(n - self.length_of_window + 1)

    def get_start_indices_for_length(self, length):
        """Return range of valid start indices for a given window length."""
        n = len(self.direction_list)
        return range(n - length + 1)

    def get_all_window_indices(self):
        """Yield (start_index, length) for every valid window of every length (1 .. n)."""
        n = len(self.direction_list)
        for length in range(1, n + 1):
            for i in range(0, n - length + 1):
                yield (i, length)

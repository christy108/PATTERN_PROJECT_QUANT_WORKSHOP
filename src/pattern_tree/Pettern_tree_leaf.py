import math


class Pettern_tree_leaf:
    """Single node in the binary tree: key, optional value, and left/right children."""

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.count = 0
        self.total_weight = 0.0
        self.ang_return = None

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_count(self):
        return self.count

    def get_total_weight(self):
        return self.total_weight

    def get_ang_return(self):
        return self.ang_return

    def set_key(self, key):
        self.key = key

    def set_value(self, value):
        self.value = value

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def set_count(self, count):
        self.count = count

    def set_total_weight(self, total_weight):
        self.total_weight = total_weight

    def set_ang_return(self, ang_return):
        self.ang_return = ang_return

    def is_leaf(self):
        return self.left is None and self.right is None

    def update_with_increment(self, increment):
        """Update count, total_weight, and ang_return from an Increment. Skip ang_return when return is NaN."""
        self.count += 1
        self.total_weight += increment.get_weights()
        ret = increment.get_returns()
        if ret is not None and not (isinstance(ret, float) and math.isnan(ret)):
            old_avg = self.ang_return if self.ang_return is not None else 0.0
            self.ang_return = old_avg + (ret - old_avg) / self.count
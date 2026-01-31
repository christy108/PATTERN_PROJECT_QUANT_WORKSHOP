from collections import deque

from .Pettern_tree_leaf import Pettern_tree_leaf


class Pettern_tree_map:
    """Binary tree map: holds the root and provides insert/search over the tree."""

    def __init__(self):
        self._root = None

    def get_root(self):
        return self._root

    def set_root(self, leaf):
        self._root = leaf

    def insert(self, key, value=None):
        """Insert a key (and optional value) into the tree. Uses key order: left < key < right."""
        if self._root is None:
            self._root = Pettern_tree_leaf(key, value)
            return
        self._insert_at(self._root, key, value)

    def _insert_at(self, leaf, key, value):
        if key < leaf.get_key():
            if leaf.get_left() is None:
                leaf.set_left(Pettern_tree_leaf(key, value))
            else:
                self._insert_at(leaf.get_left(), key, value)
        else:
            if leaf.get_right() is None:
                leaf.set_right(Pettern_tree_leaf(key, value))
            else:
                self._insert_at(leaf.get_right(), key, value)

    def search(self, key):
        """Return the leaf with the given key, or None if not found."""
        if self._root is None:
            return None
        return self._search_at(self._root, key)

    def _search_at(self, leaf, key):
        if key == leaf.get_key():
            return leaf
        if key < leaf.get_key() and leaf.get_left() is not None:
            return self._search_at(leaf.get_left(), key)
        if key > leaf.get_key() and leaf.get_right() is not None:
            return self._search_at(leaf.get_right(), key)
        return None

    def get_or_create_leaf_for_direction(self, direction):
        """From root, go left if direction == '0' else right; create child if missing. Return that leaf."""
        return self.get_or_create_leaf_for_path([direction])

    def get_or_create_leaf_for_path(self, directions):
        """Walk the tree following the sequence of directions ('0' = left, '1' = right); create nodes as needed. Return the node at the end. directions must have at least one element."""
        if not directions:
            if self._root is None:
                self._root = Pettern_tree_leaf(None, None)
            return self._root
        if self._root is None:
            self._root = Pettern_tree_leaf(None, None)
        current = self._root
        for d in directions:
            d_str = str(d)
            if d_str == "0":
                if current.get_left() is None:
                    current.set_left(Pettern_tree_leaf("0"))
                current = current.get_left()
            else:
                if current.get_right() is None:
                    current.set_right(Pettern_tree_leaf("1"))
                current = current.get_right()
        return current

    def update_leaf_for_increment(self, path, increment):
        """Get or create the leaf for the path (sequence of directions), then update it with the increment."""
        leaf = self.get_or_create_leaf_for_path(path)
        leaf.update_with_increment(increment)

    def print_tree(self):
        """Print the tree; each node shows path so far, key and calculated info (count, total_weight, avg_return)."""
        if self._root is None:
            print("(empty tree)")
            return
        self._print_node(self._root, indent=0, path=[])

    def _print_node(self, leaf, indent, path):
        prefix = "  " * indent
        path_str = "".join(path) if path else "(root)"
        label = "root" if leaf.get_key() is None else f"direction '{leaf.get_key()}'"
        print(f"{prefix}{label}  path={path_str}")
        print(f"{prefix}  count={leaf.get_count()}, total_weight={leaf.get_total_weight()}, avg_return={leaf.get_avg_return()}")
        if leaf.get_left() is not None:
            self._print_node(leaf.get_left(), indent + 1, path + ["0"])
        if leaf.get_right() is not None:
            self._print_node(leaf.get_right(), indent + 1, path + ["1"])

    def count_nodes_at_depth(self, depth):
        """Return the number of nodes at the given depth (root is depth 0)."""
        if self._root is None:
            return 0
        queue = deque([(self._root, 0)])
        count = 0
        while queue:
            node, d = queue.popleft()
            if d == depth:
                count += 1
            elif d < depth:
                if node.get_left() is not None:
                    queue.append((node.get_left(), d + 1))
                if node.get_right() is not None:
                    queue.append((node.get_right(), d + 1))
        return count

    def prune_at_depth(self, depth):
        """Remove all nodes at the given depth by clearing children of nodes at depth-1."""
        if depth <= 0 or self._root is None:
            return
        queue = deque([(self._root, 0)])
        parents = []
        while queue:
            node, d = queue.popleft()
            if d == depth - 1:
                parents.append(node)
            elif d < depth - 1:
                if node.get_left() is not None:
                    queue.append((node.get_left(), d + 1))
                if node.get_right() is not None:
                    queue.append((node.get_right(), d + 1))
        for node in parents:
            node.set_left(None)
            node.set_right(None)

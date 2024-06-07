# Only outside dep we need, to read in an existing profile


def calculate_total_time(node):
    """
    Modifies `node` inplace and adds a new key for `total_time`.
    This is calculated by summing the time (`value`) for all children
    nodes of `node` from a `tuna` trace.

    Returns:
        The modified `node`.
    """

    def _inner(node):
        if "children" in node:
            node["total_time"] = node.get("value", 0)
            for child in node["children"]:
                node["total_time"] += _inner(child)
        else:
            node["total_time"] = node.get("value", 0)
        return node["total_time"]

    _inner(node)
    return node["total_time"]


def sort_nodes_by_total_time(node):
    """
    Sort the children of `node` inplace by total time.

    Returns:
        The modified `node`.
    """

    def _inner(node):
        if "children" in node:
            node["children"] = sorted(
                node["children"], key=lambda x: x["total_time"], reverse=True
            )
            for child in node["children"]:
                _inner(child)

    _inner(node)
    return node


def find_path_by_string(node, path_string):
    """
    Returns the first path that matches `path_string` in the node.

    `path_string` should be split based on the `->` characters.

    `path_string` can also just be the name of a single `node`
    in the tree, such as instead of doing:
        `accelerate->accelerate.accelerator->torch`
    You can just do:
        `torch`

    Example:

    ```python
    from tuna_interpreter import find_path_by_string
    from tuna._import_profile import read_import_profile

    data = read_import_profile("accelerate.log")
    find_path_by_string(data, "accelerate->accelerate.accelerator->torch")
    ```
    """
    path_elements = path_string.split("->")
    current_node = node
    path_found = []

    for element in path_elements:
        if "children" not in current_node:
            return None  # Path cannot be completed, return None
        found = False
        # Use a queue to explore all possible paths
        queue = [current_node]
        while queue:
            current_node = queue.pop(0)
            if "children" not in current_node:
                return None
            for child in current_node["children"]:
                if child["text"][0] == element:
                    path_found.append(child)
                    current_node = child
                    found = True
                    break
            if found:
                break
            # If not found, add all children to the queue to check further
            queue.extend(current_node["children"])
        if not found:
            return None  # Element not found in any children, return None

    return path_found


def get_paths_above_threshold(node, threshold, max_depth, current_depth=0, path=[]):
    """
    Get all paths whos total time is below a particular threshold.
    If `threshold` is a float, then it will be interpreted as a fraction of
    the total time of all the nodes in the tree.

    Args:
        node (`dict`):
            The node to search from.
        threshold (`int` or`float`):
            The threshold to use in seconds to filter the import paths.
        max_depth (`int`):
            The maximum depth to search in the import tree.
        current_depth (`int`):
            The current depth in the import tree (used when performing recursion).
        path (`list`):
            The current path in the import tree (used when performing recursion).

    Returns:
        A list of tuples, where each tuple contains the path and the total time.
    """
    if current_depth > max_depth or "children" not in node:
        return []

    current_path = path + [node["text"][0]]
    results = []

    if node["total_time"] > threshold:
        results.append((current_path, node["total_time"]))

    for child in node["children"]:
        results.extend(
            get_paths_above_threshold(
                child, threshold, max_depth, current_depth + 1, current_path
            )
        )

    return results

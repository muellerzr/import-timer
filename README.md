# import-timer
Pragmatic approach to parsing `importtime` import profiles

While [tuna](https://github.com/nschloe/tuna/tree/main) is a fantastic way to visualize slowdowns in your python code, it lacks a native python-parsing API to allow for CI-based checks to determine or automatically flag if code is suddenly much slower (such as due to new imports). 

`import-timer` acts as a middle-ground. Create a profile using `python -X importtime`, then read it in with our utilities to help you parse and interrogate the graph by hand, establish baselines, and then let you apply these easily later in your tests.

## Installation

```bash
pip install import-timer
```

## How to Use

1. In an interactive instance, create an `importtime` log using `python -X` such as:

```python
import subprocess
output = subprocess.run(["python3", "-X", "importtime", "-c", command], capture_output=True, text=True)
```

2. Load in the logs via `import-timer`: 
```python
from import-timer import read_import_profile

data = read_import_profile(output)
```
3. Interrogate your log using our helpers.

### Supported functionality:

#### `calculate_total_time`
Will calculate the total time each tree in the `data` takes up by summing all of the times calculated down each node. This is an inplace operation, and will add a new key (`total_time`) to each node.

```python
from import_timer import read_import_profile, calculate_total_time

data = read_import_profile(...)
total_time = calculate_total_time(data)
print(total_time)
```

#### `sort_nodes_by_total_time`
Will sort all children of the passed in tree inplace based on the
total time

```python
from import_timer import read_import_profile, calculate_total_time

data = read_import_profile(...)
calculate_total_time(data)
sort_nodes_by_total_time(data)
print(data["children"][0]["total_time"])
```

### `get_paths_above_threshold`
A useful function that will take all of the nodes in `data` and then limit them to a `threshold` of which paths to return.
Helpful in cases where you only want import paths which take up >30% of the time, or a particular minimum amount of seconds to start debugging

```python
from import_timer import read_import_profile, calculate_total_time

data = read_import_profile(...)
calculate_total_time(data)
percentage_threshold = 20  # Threshold as a percentage of total time
threshold_time = total_time * (percentage_threshold / 100)  # Convert percentage to actual time threshold
max_depth = 7 # How deep in the tree do we want to report back paths
important_paths = get_paths_above_threshold(
    data_copy, threshold_time, max_depth
)
print(important_paths)
```

Explore our `tests/` to see more, or this [PR where this library was first utilized](https://github.com/huggingface/accelerate/pull/2845)
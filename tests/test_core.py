from unittest import TestCase
import copy
from tuna_interpreter.core import (
    find_path_by_string,
    calculate_total_time,
    sort_nodes_by_total_time,
    get_paths_above_threshold,
)
from tuna_interpreter import read_import_profile


class TestCore(TestCase):
    def setUp(self):
        with open("tests/artifacts/accelerate_example.log", "r") as f:
            data = f.readlines()
        self.data = read_import_profile(data)

    def test_find_path_by_string(self):
        path_nodes = find_path_by_string(
            self.data, "accelerate->accelerate.accelerator->torch"
        )
        last_value = path_nodes[-1]
        self.assertEqual(len(path_nodes), 3)
        self.assertEqual(last_value["text"], ["torch"])

    def test_calculate_total_time(self):
        data_copy = copy.deepcopy(self.data)
        calculate_total_time(data_copy)
        sort_nodes_by_total_time(data_copy)
        self.assertAlmostEqual(data_copy["children"][0]["total_time"], 0.685, 2)

    def test_threshold_filtering_pct(self):
        data_copy = copy.deepcopy(self.data)
        total_time = calculate_total_time(data_copy)
        percentage_threshold = 20  # Threshold as a percentage of total time
        threshold_time = total_time * (
            percentage_threshold / 100
        )  # Convert percentage to actual time threshold
        max_depth = 7
        important_paths = get_paths_above_threshold(
            data_copy, threshold_time, max_depth
        )
        self.assertEqual(len(important_paths), 5)

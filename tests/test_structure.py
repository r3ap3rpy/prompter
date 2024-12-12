from unittest import TestCase
from prompter.prompter import *


class Structure(TestCase):
    def setUp(self):
        self.prompt = PromptGenerator()

    def test_stats_keys(self):
        assert len(self.prompt.raw_data.keys()) > 0 

    def test_stats_keys_length(self):
        for key in self.prompt.raw_data:
            assert len(self.prompt.raw_data[key]) > 0


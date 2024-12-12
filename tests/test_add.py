from unittest import TestCase
from prompter.prompter import *
import pytest

class Addition(TestCase):
    def setUp(self):
        self.prompt = PromptGenerator()

    def test_without_args(self):
        with pytest.raises(PrompterAddError):
            self.prompt.add()

    def test_add_duplicate(self):
        with pytest.raises(PrompterAddError):
            self.prompt.add("testpeople","testactivity","testlocation")
            self.prompt.add("testpeople","testactivity","testlocation")
        self.prompt.delete('testpeople')
        self.prompt.delete('testactivity')
        self.prompt.delete('testlocation')

    def test_add_to_section_nonexistent(self):
        with pytest.raises(PrompterSectionAddException):
            self.prompt.add_to_section("nonexisten","nonexistentvalue")

    def test_add_to_section_duplicate_value(self):
        with pytest.raises(PrompterSectionAddException):
            self.prompt.add_to_section("people","Julius Caesar")

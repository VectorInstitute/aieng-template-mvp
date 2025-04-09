"""Tests for example service."""

import pytest

from services.example_service import ExampleService


class TestExampleService:
    """Tests for ExampleService."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = ExampleService()

    def test_get_all_examples(self) -> None:
        """Test getting all examples."""
        examples = self.service.get_all_examples()
        assert len(examples) == 3
        assert examples[0]["id"] == "1"
        assert examples[1]["id"] == "2"
        assert examples[2]["id"] == "3"

    def test_get_example_by_id_valid(self) -> None:
        """Test getting an example by ID with a valid ID."""
        example = self.service.get_example_by_id("1")
        assert example["id"] == "1"
        assert example["name"] == "Example 1"

    def test_get_example_by_id_invalid(self) -> None:
        """Test getting an example by ID with an invalid ID."""
        with pytest.raises(ValueError):
            self.service.get_example_by_id("999")

"""Example service module."""

from typing import Dict, List


class ExampleService:
    """Example service class.

    This is a simple example of a service class that could be used to
    implement business logic for your application.
    """

    def __init__(self) -> None:
        """Initialize the example service."""
        self.data: List[Dict[str, str]] = [
            {"id": "1", "name": "Example 1", "description": "This is example 1"},
            {"id": "2", "name": "Example 2", "description": "This is example 2"},
            {"id": "3", "name": "Example 3", "description": "This is example 3"},
        ]

    def get_all_examples(self) -> List[Dict[str, str]]:
        """Get all examples.

        Returns
        -------
        List[Dict[str, str]]
            List of all examples.
        """
        return self.data

    def get_example_by_id(self, example_id: str) -> Dict[str, str]:
        """Get an example by ID.

        Parameters
        ----------
        example_id : str
            ID of the example to retrieve.

        Returns
        -------
        Dict[str, str]
            Example data.

        Raises
        ------
        ValueError
            If the example with the given ID is not found.
        """
        for example in self.data:
            if example["id"] == example_id:
                return example
        raise ValueError(f"Example with ID {example_id} not found")

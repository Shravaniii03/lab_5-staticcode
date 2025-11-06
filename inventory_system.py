"""
Inventory Management System
---------------------------
Performs add, remove, save, load, and report functions on stock data.
Implements object-oriented design, type hints, and structured logging.
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, List, Any


class InventoryManager:
    """Handles inventory operations including add, remove, save, load, and reporting."""

    def __init__(self) -> None:
        """Initialize an empty inventory and configure logging."""
        self._stock_data: Dict[str, Dict[str, Any]] = {}
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
        self._logger = logging.getLogger(__name__)

    def add_item(self, item_name: str, tags: List[str] | None = None, quantity: int = 10) -> None:
        """Add a new item to inventory.

        Args:
            item_name (str): Name of the item.
            tags (List[str] | None): List of tags for the item.
            quantity (int): Initial stock quantity.
        """
        tags = tags or []
        if quantity < 0:
            self._logger.error("Quantity must be non-negative for item: %s", item_name)
            return

        self._stock_data[item_name] = {"quantity": quantity, "tags": tags}
        self._logger.info("Added item '%s' | Quantity: %d | Tags: %s", item_name, quantity, tags)

    def remove_item(self, item_name: str) -> None:
        """Remove an item from inventory if it exists."""
        try:
            del self._stock_data[item_name]
            self._logger.info("Removed item: %s", item_name)
        except KeyError:
            self._logger.warning("Attempted to remove non-existent item: %s", item_name)

    def get_quantity(self, item_name: str) -> int:
        """Return the quantity of a specific item."""
        return self._stock_data.get(item_name, {}).get("quantity", 0)

    def load_data(self, filename: Path = Path("stock.json")) -> None:
        """Load inventory data from a JSON file.

        Args:
            filename (Path): Path to the JSON file.
        """
        if not filename.exists():
            self._logger.warning("File not found: %s. Starting with empty inventory.", filename)
            self._stock_data.clear()
            return

        try:
            with filename.open("r", encoding="utf-8") as file:
                self._stock_data = json.load(file)
            self._logger.info("Data loaded successfully from %s", filename)
        except json.JSONDecodeError as err:
            self._logger.error("Invalid JSON in %s: %s. Starting empty.", filename, err)
            self._stock_data.clear()
        except OSError as err:
            self._logger.error("Error reading %s: %s", filename, err)
            self._stock_data.clear()

    def save_data(self, filename: Path = Path("stock.json")) -> None:
        """Save inventory data to a JSON file.

        Args:
            filename (Path): Path to save the file.
        """
        try:
            with filename.open("w", encoding="utf-8") as file:
                json.dump(self._stock_data, file, indent=4)
            self._logger.info("Data saved successfully to %s", filename)
        except OSError as err:
            self._logger.error("Failed to save data: %s", err)

    def print_data(self) -> None:
        """Display all items and quantities in the inventory."""
        if not self._stock_data:
            self._logger.info("Inventory is empty.")
            return

        self._logger.info("Inventory contents:")
        for name, details in self._stock_data.items():
            self._logger.info("%s: %d units | Tags: %s",
                              name, details["quantity"], details["tags"])

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """Check and log items with quantity below the threshold."""
        low_items = [
            name for name, details in self._stock_data.items()
            if details.get("quantity", 0) < threshold
        ]

        if low_items:
            self._logger.warning("Low stock items: %s", ", ".join(low_items))
        else:
            self._logger.info("All items are sufficiently stocked.")
        return low_items

    def __str__(self) -> str:
        """Return a readable string representation of inventory."""
        return f"InventoryManager({len(self._stock_data)} items)"


def main() -> None:
    """Demonstrate inventory system functionality."""
    manager = InventoryManager()
    manager.load_data()
    manager.add_item("Pen", tags=["stationery"], quantity=15)
    manager.add_item("Notebook", tags=["stationery"], quantity=7)
    manager.remove_item("Pencil")  # Non-existent item
    manager.print_data()
    manager.check_low_items(threshold=8)
    manager.save_data()


if __name__ == "__main__":
    main()

class ItemNotFoundError(Exception):
    """Exception for handling the case when an item is not found."""
    pass


class ItemAlreadyExistsError(Exception):
    """Exception for handling the case when an item already exists."""
    pass


class ItemNameTooShortError(Exception):
    """Exception for handling the case when the item name is too short."""
    pass

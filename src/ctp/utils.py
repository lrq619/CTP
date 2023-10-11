import logging
import sys
from typing import List, Any, Optional, Type

# Step 1: Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the desired logging level here

# Step 2: Create handlers
file_handler = logging.FileHandler('/home/lrq619/proj/CTP/logs/ctp.log')  # You can replace 'logfile.log' with your desired log file name
stdout_handler = logging.StreamHandler(sys.stdout)

# Step 3: Set log levels and formats
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

file_handler.setLevel(logging.DEBUG)  # Set desired logging level for file handler
stdout_handler.setLevel(logging.DEBUG)  # Set desired logging level for stdout handler

# Step 4: Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def can_append(o : any, l : List[any]) -> bool :
    """
    Checks if the given object o matches with the type of elements in the list l.

    Parameters:
    - o (Any): The object to check the type for.
    - l (List[Any]): The list containing elements of a specific type.

    Returns:
    - bool: True if the type of o matches the type of elements in l, or if l is empty. Otherwise, returns False.
    """
    list_type = get_type(l)
    if not list_type:
        return True  # Return True if the list is empty
    return isinstance(o, list_type)

def get_type(l: List[Any]) -> Optional[Type[Any]]:
    """
    Returns the type of the elements in the given list after ensuring all elements are of the same type.

    Parameters:
    - l (List[Any]): A list of elements.

    Returns:
    - Type[Any]: The type of the elements in the list or None if the list is empty.
    
    Raises:
    - AssertionError: If not all elements in the list are of the same type.
    """
    assert check_pure(l), "All elements in the list must be of the same type."
    return type(l[0]) if l else None

def check_pure(l: List[Any]) -> bool:
    """
    Checks if all elements in the given list are of the same type.

    Parameters:
    - l (List[Any]): A list of elements.

    Returns:
    - bool: True if all elements in the list are of the same type or the list is empty. Otherwise, returns False.
    """
    first_type = type(l[0]) if l else None
    return all(isinstance(item, first_type) for item in l)
import random
import re
from typing import Callable

def generate_nickname(is_unique: Callable[[str], bool] = None) -> str:
    """Generate a URL-safe nickname using adjectives and animal names.

    Args:
        is_unique (Callable[[str], bool], optional): A function to check nickname uniqueness. 
                                                     Defaults to None.

    Returns:
        str: A valid, unique nickname.
    """
    adjectives = ["clever", "jolly", "brave", "sly", "gentle"]
    animals = ["panda", "fox", "raccoon", "koala", "lion"]
    nickname_pattern = r'^(?![-_])[a-zA-Z0-9-_]+(?<![-_])$'

    while True:
        number = random.randint(0, 999)
        nickname = f"{random.choice(adjectives)}_{random.choice(animals)}_{number}"
        
        # Validate nickname
        if not re.match(nickname_pattern, nickname):
            continue
        
        # Ensure uniqueness (if checker is provided)
        if is_unique and not is_unique(nickname):
            continue
        
        return nickname

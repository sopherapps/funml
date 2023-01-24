from funml.utils import generate_random_string


def test_generate_random_string():
    """Generates unique random strings"""
    names = [generate_random_string() for _ in range(8)]
    assert len(set(names)) == 8

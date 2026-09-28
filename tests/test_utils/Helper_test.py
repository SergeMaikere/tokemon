import pytest
from utils.Helper import between

def test_between_max ():
	result = between(0, 100, 150)
	assert result == 100

def test_between_min ():
	result = between(0, 100, -20)
	assert result == 0


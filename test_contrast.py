import pytest
import numpy as np

def test_contrast():
    import contrast
    result = contrast.contrast([1,2,3],[2,3,4])
    assert np.all(result == [1/1.5, 1/2.5, 1/3.5])

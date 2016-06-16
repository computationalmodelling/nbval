import lib

def test_sum():
    assert lib.mysum(1, 3) == 4
    assert lib.mysum("cat", "dog") == "catdog"
    assert lib.mysum(1.5, 2) == 3.5
    

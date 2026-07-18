from src.validate_data import load_dataset


def test_dataset_acceptance_values():
    X, y = load_dataset()
    assert X.shape == (2584, 18)
    assert int(y.sum()) == 170
    assert int((y == 0).sum()) == 2414


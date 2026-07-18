from sklearn.model_selection import train_test_split
from src.v2_pipeline import build_models
from src.validate_data import load_dataset


def test_split_and_pipeline_fit_only_on_train():
    X, y = load_dataset(); Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.3, stratify=y, random_state=42)
    model = build_models()["Logistic Regression"].fit(Xtr, ytr)
    assert len(Xte) == 776 and int(yte.sum()) == 51
    assert int((yte == 0).sum()) == 725
    assert model.named_steps["preprocess"].named_transformers_["numeric"].n_samples_seen_ == len(Xtr)

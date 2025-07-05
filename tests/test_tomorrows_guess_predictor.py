from features.tomorrows_guess.predictor import get_tomorrows_prediction

def test_get_tomorrows_prediction():
    result = get_tomorrows_prediction("New York")
    assert isinstance(result, tuple)
    assert isinstance(result[0], float)  # Predicted temp
    assert isinstance(result[1], str)    # Confidence
    assert isinstance(result[2], int)    # Certainty scale

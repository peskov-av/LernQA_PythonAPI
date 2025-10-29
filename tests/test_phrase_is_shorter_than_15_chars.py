class TestPhrase:
    def test_phrase_is_shorter_than_15_chars(self):

        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15

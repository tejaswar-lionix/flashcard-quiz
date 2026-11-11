import os
import tempfile
import unittest

from quiz import add_card, check, load_deck, save_deck, score


class QuizTests(unittest.TestCase):
    def test_add_card_trims_text(self):
        cards = add_card([], "  capital of France? ", " Paris ")
        self.assertEqual(cards[0]["front"], "capital of France?")
        self.assertEqual(cards[0]["back"], "Paris")

    def test_add_card_rejects_empty_fields(self):
        with self.assertRaises(ValueError):
            add_card([], "", "answer")

    def test_check_ignores_case_and_whitespace(self):
        cards = add_card([], "capital of France?", "Paris")
        self.assertTrue(check(cards, 0, "  paris "))

    def test_score_counts_correct_answers(self):
        cards = add_card(add_card([], "2+2", "4"), "3+3", "6")
        self.assertEqual(score(cards, ["4", "wrong"]), 1)

    def test_score_requires_matching_answer_count(self):
        cards = add_card([], "2+2", "4")
        with self.assertRaises(ValueError):
            score(cards, [])

    def test_deck_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "deck.json")
            cards = add_card([], "2+2", "4")
            save_deck(cards, path)
            self.assertEqual(load_deck(path), cards)


class ShuffleTests(unittest.TestCase):
    def test_shuffle_is_deterministic_with_seed(self):
        from quiz import shuffle_cards

        cards = [{"front": str(index), "back": str(index)} for index in range(10)]
        self.assertEqual(shuffle_cards(cards, seed=7), shuffle_cards(cards, seed=7))

    def test_shuffle_changes_order(self):
        from quiz import shuffle_cards

        cards = [{"front": str(index), "back": str(index)} for index in range(10)]
        self.assertNotEqual(shuffle_cards(cards, seed=7), cards)

    def test_shuffle_does_not_mutate_input(self):
        from quiz import shuffle_cards

        cards = add_card([], "2+2", "4")
        shuffle_cards(cards, seed=1)
        self.assertEqual(len(cards), 1)


if __name__ == "__main__":
    unittest.main()

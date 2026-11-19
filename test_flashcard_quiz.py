import csv
import os
import tempfile
import unittest

from quiz import (
    add_card,
    check,
    delete_card,
    edit_card,
    export_csv,
    import_csv,
    load_deck,
    retry_queue,
    run_round,
    save_deck,
    score,
)


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


class EditCardTests(unittest.TestCase):
    def test_edit_both_fields(self):
        cards = add_card([], "2+2", "4")
        result = edit_card(cards, 0, front=" 3+3 ", back=" 6 ")
        self.assertEqual(result[0]["front"], "3+3")
        self.assertEqual(result[0]["back"], "6")

    def test_edit_one_field_leaves_other_unchanged(self):
        cards = add_card([], "2+2", "4")
        edit_card(cards, 0, front=" 3+3 ")
        self.assertEqual(cards[0]["front"], "3+3")
        self.assertEqual(cards[0]["back"], "4")

    def test_edit_blank_field_raises(self):
        cards = add_card([], "2+2", "4")
        with self.assertRaises(ValueError):
            edit_card(cards, 0, front="   ")
        with self.assertRaises(ValueError):
            edit_card(cards, 0, back="")


class DeleteCardTests(unittest.TestCase):
    def test_delete_middle_card(self):
        cards = add_card(add_card(add_card([], "one", "1"), "two", "2"), "three", "3")
        self.assertEqual(
            [card["front"] for card in delete_card(cards, 1)],
            ["one", "three"],
        )

    def test_delete_only_card(self):
        cards = add_card([], "one", "1")
        self.assertEqual(delete_card(cards, 0), [])

    def test_delete_out_of_range_raises(self):
        with self.assertRaises(IndexError):
            delete_card([], 0)


class CsvDeckTests(unittest.TestCase):
    def test_export_import_roundtrip(self):
        cards = add_card(add_card([], "2+2", "4"), "capital, France?", "Paris")
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "deck.csv")
            export_csv(cards, path)
            self.assertEqual(import_csv(path), cards)

    def test_import_blank_cell_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "deck.csv")
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["front", "back"])
                writer.writerow(["2+2", ""])
            with self.assertRaises(ValueError):
                import_csv(path)

    def test_import_preserves_order(self):
        cards = add_card(add_card(add_card([], "one", "1"), "two", "2"), "three", "3")
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "deck.csv")
            export_csv(cards, path)
            imported = import_csv(path)
        self.assertEqual([card["front"] for card in imported], ["one", "two", "three"])


class RoundTests(unittest.TestCase):
    def test_round_reports_correct_and_missed(self):
        cards = add_card(add_card([], "2+2", "4"), "3+3", "6")
        result = run_round(cards, ["4", "wrong"])
        self.assertEqual(result["correct"], 1)
        self.assertEqual(result["total"], 2)
        self.assertEqual(len(result["missed"]), 1)
        self.assertEqual(result["missed"][0]["front"], "3+3")

    def test_retry_queue_returns_only_wrong_cards(self):
        cards = add_card(add_card([], "2+2", "4"), "3+3", "6")
        self.assertEqual(retry_queue(cards, ["wrong", "6"]), [cards[0]])

    def test_retry_queue_empty_after_all_correct(self):
        cards = add_card(add_card([], "2+2", "4"), "3+3", "6")
        self.assertEqual(retry_queue(cards, ["4", "6"]), [])

    def test_round_requires_matching_answer_count(self):
        cards = add_card([], "2+2", "4")
        with self.assertRaises(ValueError):
            run_round(cards, [])


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

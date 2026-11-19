#!/usr/bin/env python3
"""Flashcards with simple answer checking and scoring."""
import csv
import json
import os

DEFAULT_PATH = os.path.expanduser("~/.flashcards.json")


def load_deck(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save_deck(cards, path=DEFAULT_PATH):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(cards, handle, indent=2)


def add_card(cards, front, back):
    if not front.strip() or not back.strip():
        raise ValueError("front and back must not be empty")
    cards.append({"front": front.strip(), "back": back.strip()})
    return cards


def edit_card(cards, index, front=None, back=None):
    updates = {}
    if front is not None:
        front = front.strip()
        if not front:
            raise ValueError("front and back must not be empty")
        updates["front"] = front
    if back is not None:
        back = back.strip()
        if not back:
            raise ValueError("front and back must not be empty")
        updates["back"] = back
    cards[index].update(updates)
    return cards


def delete_card(cards, index):
    cards.pop(index)
    return cards


def export_csv(cards, path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["front", "back"])
        for card in cards:
            writer.writerow([card["front"], card["back"]])
    return path


def import_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        cards = []
        for row in reader:
            cards = add_card(cards, row["front"], row["back"])
    return cards


def check(cards, index, answer):
    expected = cards[index]["back"].strip().lower()
    return answer.strip().lower() == expected


def score(cards, answers):
    if len(cards) != len(answers):
        raise ValueError("one answer per card is required")
    return sum(check(cards, index, answer) for index, answer in enumerate(answers))


def run_round(cards, answers):
    if len(cards) != len(answers):
        raise ValueError("one answer per card is required")
    missed = [
        card
        for index, card in enumerate(cards)
        if not check(cards, index, answers[index])
    ]
    return {"correct": len(cards) - len(missed), "total": len(cards), "missed": missed}


def retry_queue(cards, answers):
    return run_round(cards, answers)["missed"]


def shuffle_cards(cards, seed=None):
    """Return a shuffled copy of cards. Seed makes the order deterministic."""
    import random

    shuffled = list(cards)
    random.Random(seed).shuffle(shuffled)
    return shuffled

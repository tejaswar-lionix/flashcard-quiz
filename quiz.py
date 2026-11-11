#!/usr/bin/env python3
"""Flashcards with simple answer checking and scoring."""
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


def check(cards, index, answer):
    expected = cards[index]["back"].strip().lower()
    return answer.strip().lower() == expected


def score(cards, answers):
    if len(cards) != len(answers):
        raise ValueError("one answer per card is required")
    return sum(check(cards, index, answer) for index, answer in enumerate(answers))

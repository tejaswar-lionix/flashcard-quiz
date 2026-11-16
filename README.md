# flashcard-quiz

Flashcards with answer checking, scoring, and shuffling.

## Usage

```bash
python3 -c "from quiz import *; c=add_card([], '2+2', '4'); print(score(c, ['4']))"
python3 -c "from quiz import *; c=add_card([], '2+2', '4'); print(run_round(c, ['4']))"
```

## Features

- Card creation with validated fields
- Case-insensitive answer checking
- Deterministic shuffling with shuffle_cards(cards, seed=...)
- Rounds with run_round(cards, answers) and retry_queue(cards, answers)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT

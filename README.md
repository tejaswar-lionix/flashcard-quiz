# flashcard-quiz

Flashcards with answer checking, scoring, and shuffling.

## Usage

```bash
python3 -c "from quiz import *; c=add_card([], '2+2', '4'); print(score(c, ['4']))"
python3 -c "from quiz import *; c=add_card([], '2+2', '4'); print(run_round(c, ['4']))"
python3 -c "from quiz import *; c=add_card([], '2+2', '4'); print(delete_card(c, 0))"
python3 -c "from quiz import *; export_csv(import_csv('deck.csv'), 'copy.csv')"
```

## Features

- Card creation with validated fields
- Card deletion by index with delete_card(cards, index)
- Case-insensitive answer checking
- Deterministic shuffling with shuffle_cards(cards, seed=...)
- Rounds with run_round(cards, answers) and retry_queue(cards, answers)
- CSV deck import and export with import_csv(path) and export_csv(cards, path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT

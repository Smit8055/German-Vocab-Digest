# German Vocabulary Digest

A Python tool that helps me study German by automatically extracting vocabulary from texts I'm reading.

## What it does
- Takes a German text (from textbooks, articles, etc.)
- Sends it to the Gemini API for a simplified summary and vocabulary extraction
- Automatically saves new words (word, meaning, example sentence) to a running CSV log
- Skips words already logged, avoiding duplicates

## Tech used
- Python
- Google Gemini API (google-genai)
- CSV for data storage

## Example output
| German word | Meaning | Example sentence |
|---|---|---|
| das Gewässer | body of water | Deutschland hat viele schöne Gewässer. |
| jedoch | however / though | Ich möchte kommen, ich habe jedoch keine Zeit. |

## How it works
1. Paste German text into `german_text.txt`
2. Run `python german_learn.py`
3. New vocabulary is appended to `german_vocab_log.csv`, duplicates automatically skipped

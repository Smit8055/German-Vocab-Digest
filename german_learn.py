from google import genai
import csv
import os
from datetime import datetime

# ---------------------------------------------------------
# STEP 1: Setting up the Gemini client
# ---------------------------------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------
# STEP 2: German text reading
# ---------------------------------------------------------
def read_german_text(filepath="german_text.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------
# STEP 3: Send it to Gemini with clear instructions
# ---------------------------------------------------------
def analyze_text(german_text):
    prompt = f"""You are a German teacher helping an A1/A2 learner.
Given the German text below, do three things:

1. Write a SIMPLE German summary (max 3 sentences, A2-level vocabulary).
2. List 5-8 useful or difficult words from the text as: German word | English meaning
3. Give ONE example sentence for each listed word (simple, A2-level).

Reply in this exact format:

SUMMARY:
<summary here>

VOCABULARY:
word1 | meaning1 | example sentence1
word2 | meaning2 | example sentence2
(etc.)

Text to analyze:
{german_text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

# ---------------------------------------------------------
# STEP 4: Parse the vocabulary lines out of the reply
# ---------------------------------------------------------
def parse_vocab(result_text):
    vocab_rows = []
    in_vocab_section = False
    for line in result_text.strip().split("\n"):
        if line.startswith("VOCABULARY"):
            in_vocab_section = True
            continue
        if in_vocab_section and "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 3:
                vocab_rows.append(parts)
    return vocab_rows

# ---------------------------------------------------------
# STEP 5: Save vocabulary to a running CSV log
# ---------------------------------------------------------
def save_to_csv(vocab_rows, filepath="german_vocab_log.csv"):
    file_exists = os.path.isfile(filepath)

    # Step 1: Load words already in the log (if the file exists)
    existing_words = set()
    if file_exists:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header row
            for row in reader:
                if row:  # skip empty lines
                    existing_words.add(row[1])  # column 1 = "German word"

    # Step 2: Filter out words that are already logged
    new_rows = [
        (word, meaning, example)
        for word, meaning, example in vocab_rows
        if word not in existing_words
    ]

    # Step 3: Append only the new words
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "German word", "Meaning", "Example sentence"])
        date_str = datetime.now().strftime("%Y-%m-%d")
        for word, meaning, example in new_rows:
            writer.writerow([date_str, word, meaning, example])

    print(f"Added {len(new_rows)} new words ({len(vocab_rows) - len(new_rows)} already existed, skipped)")
# ---------------------------------------------------------
# STEP 6: Run everything
# ---------------------------------------------------------
if __name__ == "__main__":
    text = read_german_text()
    print("Sending to Gemini...")

    result = analyze_text(text)
    print("\n--- Result ---")
    print(result)

    vocab_rows = parse_vocab(result)
    save_to_csv(vocab_rows)
    print(f"\nSaved {len(vocab_rows)} words to german_vocab_log.csv")
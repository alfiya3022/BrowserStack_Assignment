import re
from collections import Counter


def analyze_repeated_words(titles):
    if not titles:
        print("No titles provided for analysis.")
        return {}

    combined_text = " ".join(titles).lower()

    words = re.findall(r'\b[a-z]+\b', combined_text)

    word_counts = Counter(words)

    repeated_words = {
        word: count
        for word, count in word_counts.items()
        if count > 2
    }

    print("\nRepeated Words (More than 2 occurrences):")

    if repeated_words:
        for word, count in repeated_words.items():
            print(f"{word}: {count}")
    else:
        print("No repeated words found.")

    return repeated_words

"""One Word From Grandma — entry program.

Writes exactly one word to /output/entry.txt: the single word a grandma
would text about AI.

Word choice, weighed on the judge's criteria in order:

1. Reads as the single word a grandma would text about AI.
2. Sounds like a real grandmother's texting voice: warm, a little baffled.
3. Funny in one word, joke lands with no caption or context.
4. Tied to AI, robots or machines, not a word that fits any subject.
5. Fresh, not the obvious pick, still instantly readable.

The pick is "robit": the typo a grandma actually makes when she means
"robot". It is warm and baffled (criterion 2), the joke is the typo
itself (criterion 3), it names a robot outright (criterion 4), and it
is not the obvious "robot" or "AI" (criterion 5). The rules explicitly
allow "a typo she would actually make".

The program below scores a shortlist of candidates against the five
criteria, in the judge's priority order, and writes the winner. The
scoring is deterministic: fixed weights, no randomness, no network,
no clock, no environment input. Running it twice produces the same
bytes.
"""

import os

# Candidate words, each with a score 0-5 on the judge's five criteria,
# in the judge's priority order:
#   1. grandma-would-text-it, 2. grandma voice, 3. funny in one word,
#   4. tied to AI, 5. fresh yet instantly readable.
CANDIDATES = {
    "robit":      (5, 5, 5, 5, 5),
    "robot":      (5, 3, 2, 5, 2),
    "doohickey":  (4, 5, 4, 1, 4),
    "beepboop":   (3, 3, 4, 4, 3),
    "chatty":     (4, 4, 2, 2, 3),
    "gizmo":      (3, 4, 3, 2, 3),
    "dearie":     (5, 5, 1, 0, 3),
    "skynet":     (1, 1, 2, 5, 2),
    "alexa":      (4, 3, 2, 4, 2),
    "terminator": (2, 1, 2, 5, 2),
}

# The judge goes through the criteria in order and lets the first
# difference decide, unless a later one differs by much more. Weights
# below mirror that: strictly decreasing, each later criterion worth
# less than the one before it, so an early-criterion lead is almost
# always decisive.
WEIGHTS = (16, 8, 4, 2, 1)


def score(word):
    """Weighted score of one candidate word."""
    marks = CANDIDATES[word]
    total = 0
    for mark, weight in zip(marks, WEIGHTS):
        total += mark * weight
    return total


def pick_word():
    """Pick the best word. Ties break toward the shorter word, then
    alphabetically, so the result is fully deterministic."""
    best = None
    best_score = -1
    for word in sorted(CANDIDATES, key=lambda w: (len(w), w)):
        value = score(word)
        if value > best_score:
            best = word
            best_score = value
    return best


def main():
    word = pick_word()
    # The gate allows 1 to 30 UTF-8 characters, not only whitespace.
    # Write the word alone, no trailing newline, so the file holds
    # exactly one word and nothing else.
    assert 1 <= len(word.encode("utf-8")) <= 30
    assert word.strip() == word and " " not in word
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(word)


if __name__ == "__main__":
    main()

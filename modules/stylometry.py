import re

def average_word_length(text):

    words = text.split()

    if len(words) == 0:
        return 0

    total = sum(len(word) for word in words)

    return total / len(words)


def punctuation_density(text):

    punctuation = re.findall(
        r"[!?.,;:]",
        text
    )

    if len(text) == 0:
        return 0

    return len(punctuation) / len(text)


def stylometry_score(text1, text2):

    avg1 = average_word_length(text1)
    avg2 = average_word_length(text2)

    punct1 = punctuation_density(text1)
    punct2 = punctuation_density(text2)

    avg_score = 1 - (
        abs(avg1 - avg2)
        /
        max(avg1, avg2, 1)
    )

    punct_score = 1 - (
        abs(punct1 - punct2)
        /
        max(punct1, punct2, 0.01)
    )

    final = (
        avg_score +
        punct_score
    ) / 2

    return round(final,3)
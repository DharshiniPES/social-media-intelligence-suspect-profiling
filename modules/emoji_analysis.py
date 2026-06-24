import emoji

def extract_emojis(text):

    emojis = []

    for char in text:

        if char in emoji.EMOJI_DATA:
            emojis.append(char)

    return emojis


def emoji_score(text1, text2):

    emojis1 = extract_emojis(text1)
    emojis2 = extract_emojis(text2)

    set1 = set(emojis1)
    set2 = set(emojis2)

    if len(set1.union(set2)) == 0:
        return 0

    score = (
        len(set1.intersection(set2))
        /
        len(set1.union(set2))
    )

    return round(score, 3)
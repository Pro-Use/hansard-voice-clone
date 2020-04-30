
keyword_replacements = {
    "i": "you",
    "we": "you",
    "she": "you",
    "he": "you",
    "me": "you",
    "him": "you",
    "they": "you",
    "us": "you",
    "she's": "you're",
    "i'm": "you're",
    "we're": "you're",
    "he's": "you're",
    "they're": "you're",
    "his": "your",
    "her": "your",
    "their": "your",
    "our": "your",
    "i've": "you've",
    "we've": "you've",
    "they've": "you've",
}

second_replacements = {
    "am": "are",
    "is": "are",
}

keywords = keyword_replacements.keys()
second_words = second_replacements.keys()
punctuation = [".", ",", ":", ";", "!", "*"]


def replace_words(statements):
    new_statements = []
    for statement in statements:
        words = statement[1].split(' ')
        new_text = ""
        last_char = ""
        for i in range(len(words)):
            # Check previous last char for full stops
            if last_char == ".":
                capitalised = True
                words[i] = words[i].lower()
            else:
                capitalised = False
            if words[i][-1] in punctuation:
                last_char = words[i][-1]
                words[i] = words[i][:-1]
            else:
                last_char = ""
            if words[i] in keywords:
                words[i] = keyword_replacements[words[i]]
                if i != len(words) - 1 and words[i + 1] in second_words:
                    words[i + 1] = second_replacements[words[i + 1]]
            if capitalised:
                words[i] = words[i][:1].upper() + words[i][1:]
            new_text += words[i] + last_char + " "
        new_statements.append([statement[0], new_text])

    return new_statements

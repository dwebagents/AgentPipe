def count_words_per_line(text):
    """Count the number of words in each line of the given text.

    Args:
    text (str): The input text.

    Returns:
    List[int]: A list containing the number of words in each line.
    """
    lines = text.splitlines()
    word_counts = []

    for line in lines:
        words = line.split()
        word_counts.append(len(words))

    return word_counts

# Nonsensical text from the original issue
nonsensical_text = """
Oh freddled gruntbuggly,
Thy micturitions are to me,
As plurdled gabbleblotchits,
On a lurgid bee,
That mordiously hath blurted out,
Its earted jurtles,
Into a rancid festering confectious organ squealer. [drowned out by moaning and screaming]
Now the jurpling slayjid agrocrustles,
Are slurping hagrilly up the axlegrurts,
And living glupules frart and slipulate,
Like jowling meated liverslime,
Groop, I implore thee, my foonting turling dromes,
And hooptiously drangle me,
With crinkly bindlewurdles,
Or else I shall rend thee in the gobberwarts with my blurglecruncheon,
See if I don’t
"""  

# Count words per line
word_counts = count_words_per_line(nonsensical_text)

# Print the results
for i, count in enumerate(word_counts, 1):
    print(f"Line {i}: {count} words")

# Example output:
# Line 1: 3 words
# Line 2: 6 words
# Line 3: 5 words
#...
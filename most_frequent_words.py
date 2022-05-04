import table as tbl
import matplotlib.pyplot as plt
from heapq import nlargest


# Sources consulted on zip() function with * operator:
# - https://docs.python.org/3/library/functions.html#zip
# - https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/

# Source consulted on heapq.nlargest() function: https://docs.python.org/3/library/heapq.html#heapq.nlargest

# Source consulted on sorting a list of tuples:
# https://www.kite.com/python/answers/how-to-sort-a-list-of-tuples-by-the-second-value-in-python

def word_frequencies(file_path, root, minimum_word_length=0):
    """Create a BST with all the words in file_path (separated by a new line), with a length larger than or equal to
    the minimum_word_length as the keys, and the amount that they occur as the value. (Words are case insensitive.)"""

    try:
        with open(file_path) as file:

            for word in file:
                word = word.strip()  # remove \n from word

                if len(word) >= minimum_word_length:

                    # Add the word key, with a value of 1, to the BST if it doesn't exist yet..
                    # If it does, increment the value of this word key by 1.
                    tbl.add_or_increase(root, word)

    except IOError:
        raise IOError(f"Could not open {file_path}")


def top_10_most_frequent_words(file_path, minimum_word_length=0):
    """Create a list of tuples with the 10 most frequently used words and their amount of occurrences in file_path,
    with a minimum word length larger than or equal to minimum_word_length."""

    root = tbl.new_empty_root()
    most_frequent_words = []

    try:
        word_frequencies(file_path, root, minimum_word_length=minimum_word_length)

    except IOError as e:
        raise e  # If the word_frequencies() function errors out, re-raise the error it gives

    all_pairs = tbl.get_all_pairs(root)  # A list of tuples: (word, amount_of_occurrences)

    # Unzip the above tuples into a list of 2 tuples: [(words), (amount_of_occurrences)]
    unzipped_data = list(zip(*all_pairs))

    words = unzipped_data[0]
    occurrences = unzipped_data[1]

    highest_occurrences = nlargest(10, occurrences)  # Grab the 10 highest occurrences

    # Scroll through the list, and get the indexes for the highest occurrences. These indexes are also the indexes
    # of the words corresponding to these occurrences. We cannot use .index(), because if two words have the same
    # amount of occurrences, this will only get one word. (.index() returns the index of the first corresponding
    # element in the list)

    for word_index, occurrence in enumerate(occurrences):
        if occurrence in highest_occurrences:
            most_frequent_words.append((words[word_index], occurrence))

    most_frequent_words.sort(key=lambda x: x[1], reverse=True)

    return most_frequent_words


def write_most_frequent_words(words, file_path):
    """Write the supplied words and their amount of occurrences created by the top_10_most_frequent_words() function
    to file_path"""

    try:
        with open(file_path, "w") as file:

            for word, occurrence in words:

                file.write(f"{word} : {occurrence}\n")

    except IOError:
        raise IOError(f"Could not open {file_path}")


def main():
    files_and_names = (("./large_texts/holy_grail_words.lst", "Monty Python and the Holy Grail"),
                       ("./large_texts/eng_news_100K-sentences_words.lst", "100K sentences in English news"))

    for file, name in files_and_names:

        try:
            most_frequent_words = top_10_most_frequent_words(file, minimum_word_length=5)
            file_path = f"./text_analysis_results/{name} ten most frequently occurring words.txt"
            write_most_frequent_words(most_frequent_words, file_path)

        except IOError as e:
            print(f"IOError: {e}")


if __name__ == '__main__':
    main()

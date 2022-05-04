import re

# Source consulted for the regex: https://docs.python.org/3/library/re.html


def text_to_word_list(file_path):
    """
    Writes all the alphabetic words in file_path to a .lst file, seperated by a white line.

    -Words with an apostrophe will be written without an apostrophe
    -Case insensitive, so "Hello" and "hello" will be the same word
    -Words like "test-case" will be counted as two words, "test" and "case"

    :param file_path: The file containing words
    """

    try:
        with open(file_path) as read_file:

            try:
                with open(file_path.replace(".txt", "_words.lst"), "w") as write_file:

                    for line in read_file:

                        # Replace all characters from the current line with white spaces, except for alphabetic
                        # characters and apostrophes. Then remove the apostrophes, convert it to lower case,
                        # and split into a list of words. This way, the word "test-case" will be counted as
                        # two different words and "can't" will be one word. For more info, please see our report.
                        words = re.sub("[^a-zA-Z']", " ", line).replace("'", "").lower().split()

                        for word in words:
                            write_file.write(word + "\n")

            except IOError:
                raise IOError(f"Cannot write to {file_path.replace('.txt', '_words.lst')}")

    except IOError:
        raise IOError(f"Cannot read from {file_path}")

import table as tbl
import matplotlib.pyplot as plt

# Sources consulted on zip() function with * operator:
# - https://docs.python.org/3/library/functions.html#zip
# - https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/

# Sources consulted on plotting histograms with matplotlib:
# - https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.bar.html
# - https://www.tutorialspoint.com/matplotlib/matplotlib_bar_plot.htm

# Source consulted on matplotlib subplots: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.subplots.html

def count_word_lengths(file_path, root):
    """Count the length of the words in file_path (separated by new lines) and add them to the BST,
    with the word length as the key and the count as the value. """

    try:
        with open(file_path) as file:
            for word in file:
                word_length = len(word.strip())

                # Add the word_length key, with a value of 1, to the BST if it doesn't exist yet.
                # If it does, increment the value of this word_length key by 1.
                tbl.add_or_increase(root, word_length)

    except IOError:
        raise IOError(f"Could not open {file_path}")


def word_lengths_histogram(file_path, graph):
    """Plot a histogram for the word lengths and their count in file_path (words separated by a new line)."""

    root = tbl.new_empty_root()

    try:
        count_word_lengths(file_path, root)

    except IOError as e:
        raise e  # If the count_word_lengths() function errors out, re-raise the error it gives

    all_pairs = tbl.get_all_pairs(root)  # A list of tuples: (word_length, count)
    count = list(zip(*all_pairs))  # Unzip the above tuples into a list of 2 tuples: [(word_lengths), (counts)]
    
    graph.grid(True, which='both',zorder=0) # Grid under the bar plot with zorder
    graph.set_xlabel("Word lengths")
    graph.set_ylabel("Count")
    graph.set_xticks(count[0])
    graph.bar(count[0], count[1], zorder=3)  #add log=True for log scale y axis
    # The word lengths on the x-axis, and their count as the height of the bar                                             


def main():
    fig, (holy_grail, eng_news) = plt.subplots(ncols=1, nrows=2, constrained_layout=True)

    files_graphs_names = (("/large_texts/holy_grail_words.lst", holy_grail, "Holy Grail"),
                        ("./large_texts/eng_news_100K-sentences_words.lst", eng_news, "English news"))

    for file, graph, name in files_graphs_names:

        try:
            word_lengths_histogram(file, graph)
            graph.title.set_text(name)

        except IOError as e:
            print(f"IOError: {e}")

    fig.set_figwidth(14)
    plt.savefig("./text_analysis_results/word_lengths.png")

if __name__ == '__main__':
    main()

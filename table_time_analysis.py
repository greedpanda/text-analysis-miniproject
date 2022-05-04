import table as tbl
import matplotlib.pyplot as plt
import time

# Sources consulted on zip() function with * operator:
# - https://docs.python.org/3/library/functions.html#zip
# - https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/

# Source consulted on matplotlib subplots: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.subplots.html


def measure_time(words, look_up_words):
    """Return a list of tuples with time analysis for looking up words in a BST of file_path
    (words separated by a new line). List is in a form of:
    [(table_size1, time1), (table_size2, time2), ..., (table_sizeN, timeN)]"""

    root = tbl.new_empty_root()

    # Look up time vs table size
    time_size = []

    words_added = 0

    for word in words:

        tbl.add(root, word.strip(), 0)  # Value is not relevant

        words_added += 1

        # If a multiple of 1000 words have been added, add data to the list
        if words_added % 1000 == 0:
            start = time.time()

            for look_up_word in look_up_words:

               tbl.get(root, look_up_word)

            end = time.time()
            total_time = round(end - start, 3)  # Measure the time elapsed since start time

            time_size.append((words_added, total_time))

    return time_size


def measure_depth(words):
    """Return a list of tuples with depth analysis for looking up words in a BST of file_path
    (words separated by a new line). List is in a form of:
    [(table_size1, depth1), (table_size2, depth2), ..., (table_sizeN, depthN)]"""

    root = tbl.new_empty_root()

    # Max depth vs size
    depth_size = []

    words_added = 0

    for word in words:

        tbl.add(root, word.strip(), 0)  # Value is not relevant

        words_added += 1

        # If a multiple of 1000 words have been added, add data to the list
        if words_added % 1000 == 0:
            depth_size.append((words_added, tbl.max_depth(root)))

    return depth_size


def main():

    words = []
    look_up_words = []

    # Get the words to add to the BST. This is a shuffled list of the unique words in
    # ./large_texts/eng_news_100K-sentences.words.lst

    # Bash command used:
    # sort eng_news_100K-sentences_words.lst | uniq | sort -R > eng_news_100K-sentences_words_unique.lst
    with open("./large_texts/eng_news_100K-sentences_words_unique.lst") as file:
        for word in file:
            words.append(word.strip())

    # Get the words to look up in the BST. These are 20000 randomly selected words in the unique words of
    # ./large_texts/eng_news_100K-sentences.words.lst

    # Bash command used:
    # shuf -n 20000 eng_news_100K-sentences_words_unique.lst > look_up_words.lst
    with open("./large_texts/look_up_words.lst") as file:
        for word in file:
            look_up_words.append(word.strip())

    # We want to measure the time multiple times and compute an average, to try to negate the influence that the OS
    # background processes have on the execution time

    amount_of_measurements = 50
    execution_time = []

    for _ in range(amount_of_measurements):

        # Get a list of tuples:
        # [(table_size1, time1), (table_size2, time2), ..., (table_sizeN, timeN)]
        data = measure_time(words, look_up_words)

        # Unzip the list of tuples into a list of two tuples:
        # [(table_sizes), (times)]
        unzipped_data = list(zip(*data))

        if execution_time:  # If the list has been initialized, we add the numbers
            for i, exec_time in enumerate(unzipped_data[1]):  # Loop through the execution times
                execution_time[i] += exec_time

        else:  # If the list has not been initialized yet, we initialize it
            for exec_time in unzipped_data[1]:  # Loop through the execution times
                execution_time.append(exec_time)

    execution_time = [t / amount_of_measurements for t in execution_time]  # Compute the averages

    # Get a list of tuples:
    # [(table_size1, depth1), (table_size2, depth2), ..., (table_sizeN, depthN)]
    depth_data = measure_depth(words)

    # Unzip the list of tuples into a list of two tuples:
    # [(table_sizes), (depths)]
    unzipped_depth_data = list(zip(*depth_data))

    sizes = unzipped_depth_data[0]
    depths = unzipped_depth_data[1]

    fig, (time_analysis, depth_analysis) = plt.subplots(nrows=1, ncols=2, constrained_layout=True)

    time_analysis.plot(sizes, execution_time)
    time_analysis.set_xlabel("Table size")
    time_analysis.set_ylabel("Time used to get 20000 elements")

    depth_analysis.plot(sizes, depths)
    depth_analysis.set_xlabel("Table size")
    depth_analysis.set_ylabel("BST depth")

    plt.savefig("./BST_time_analysis.png")


if __name__ == '__main__':
    main()

import word_set as ws
import matplotlib.pyplot as plt
import time
import os
import numpy

# Program stars


# Printing function for count of unique words, the max bucket size and the total size of the buckets.
def printing(word_set_to_print):
    print(f"\nCount: {ws.count(word_set_to_print)}")
    mx = ws.max_bucket_size(word_set_to_print)
    print(f"Max bucket: {mx}")                
    buckets = ws.bucket_list_size(word_set_to_print)
    print(f"Bucket list size: {buckets}")


# Absolute path fetcher function
def abs_path_fetch(local_address):
    absolute_dir = os.path.dirname(__file__)
    relative_path = local_address
    absolute_file_path = os.path.join(absolute_dir, relative_path)
    return absolute_file_path


#############################################################
### Hashing table of the 100k sentences - time experiment ###
#############################################################


# X axis
x_size1 = [0]       # Initializing list for storing size each hundred words (needed for plot)
x_size2 = [0]       # Initializing list for storing size each thousand words (needed for plot)
x_buckets = [10]    # Initializing list for storing number of buckets each rehash (needed for plot)
x_max_bucket = []

# Y axis
time_t1 = [0]  # Initializing list for storing timestamps of each hundred words (needed for plot)
time_t2 = [0]  # Initializing list for storing timestamps of each thousand words (needed for plot)
time_t3 = [0]  # Initializing list for storing timestamps of each rehashing (needed for plot)

# Auxiliary variables initialization
aux_hundred = 100       # Initializing aux var for hundred words
aux_thousand = 1000     # initializing aux var for thousand words
aux_max_buckets = 10     # Initializing aux var number of buckets


with open(abs_path_fetch("large_texts/eng_news_100K-sentences_words.lst")) as words_list:
    word_set = ws.new_empty_set()

    # Setting initial timestamp for initial data reference
    start_time_100k = time.time()  
    timestamp_100k = start_time_100k
    timestamp2_100k = start_time_100k
    timestamp3_100k = start_time_100k

    for word in words_list: 
        ws.add(word_set, word)

        # Storing size and timestamp every new unique 100 words added
        if ws.size == aux_hundred:
            aux_hundred += 100
            x_size1.append(aux_hundred)
            time_t1.append((time.time() - timestamp_100k) * 1000)  # Multiplied by 1000 to represent time in millisecond
            timestamp_100k = time.time()

        # Storing size and timestamp every new unique 1000 words added
        if ws.size == aux_thousand:
            aux_thousand += 1000
            x_size2.append(aux_thousand)
            time_t2.append((time.time() - timestamp2_100k ) * 1000)
            timestamp2_100k = time.time()

        # Storing max bucket size and timestamp every rehash
        if ws.size == aux_max_buckets:
            x_max_bucket.append(ws.max_bucket_size(word_set))
            aux_max_buckets *= 2
            x_buckets.append(aux_max_buckets)
            time_t3.append((time.time() - start_time_100k) * 1000)
    
    x_max_bucket.append(ws.max_bucket_size(word_set)) 	# Adding the last max bucket size


# HSTB = hash set total buckets
# MBS = max bucket size
# for i in range(len(time_t3)):
#     print(f'HSTB {x_buckets[i]} : MBS {x_max_bucket[i]}')
# printing(word_set)

elapsed_time_100k = round(time.time() - start_time_100k, 3)  # Computing the time needed to complete the entire hashing
print(f"Elapsed time in seconds for hashing the 100k sentences list file is: {elapsed_time_100k}\n")


################
### Plotting ###
################

# Source: https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.subplots.html

# Figure 1 in 2 rows, 1 column, layout constrained to avoid overlap and x axis shared
fig1, bt = plt.subplots(nrows=2, ncols=1, constrained_layout=True, sharex=True)

# bt[0] will be the subplot for the function of number of words (100 and 1000) over time
# bt[1] will be the subplot for the function of max number of buckets over time


# Plot style function
def plot_style(ax):
    ax.set_xticks(numpy.arange(0, 83000, 1000))           # Ticks in x axis every 1000 buckets
    ax.tick_params(labelsize='small', rotation=90)        # Ticks set to small and rotated
    ax.set_xlabel('size', size='small')                   # X axis label (size) set to small
    ax.set_ylabel('time [ms]', size='small')              # Y axis label (time in millisecond) set to small
    ax.legend(loc='upper left')                           # Fixing the location of the legend on the upper left position
    ax.grid(True, which="both")                           # Setting the grid for every tick


# bt[0] plot for 'number of words' over 'time'

# Plotting blue dots labeled '100 words'
bt[0].plot(x_size1, time_t1, color='tab:blue', marker='.', label='N = 100 words')

# Plotting red dots labeled '1000 words'
bt[0].plot(x_size2, time_t2, color='tab:red', marker='.', label='N = 1000 words')
bt[0].set_title('N element added / Time')  # Setting the title
plot_style(bt[0])

# bt[1] plot for 'max number of buckets' over 'time'

# Plotting red dots labeled 'Buckets'
bt[1].step(x_buckets, time_t3, color='tab:red', marker='.', label='Buckets')

# Setting the title
bt[1].set_title('Bucket size / Time')
plot_style(bt[1])

# Annotation for max bucket size
# for i in range(len(time_t3)):
#     bt[1].text(x_buckets[i],time_t3[i],f'{x_max_bucket[i]}',wrap=True, size='small')

plt.show()  # Calling the plot on a popup window

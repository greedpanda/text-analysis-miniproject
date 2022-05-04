import word_set as ws
import os

# Program stars


# Printing function for count of unique words, the max bucket size and the total size of the buckets.
def printing(word_set_to_print):
    print(f"\nUnique words: {ws.count(word_set_to_print)}")
    mx = ws.max_bucket_size(word_set_to_print)
    print(f"Max bucket: {mx}")                
    buckets = ws.bucket_list_size(word_set_to_print)
    print(f"Bucket list size: {buckets}\n")


# Absolute path fetcher function
def abs_path_fetch(local_address):
    absolute_dir = os.path.dirname(__file__)
    relative_path = local_address
    absolute_file_path = os.path.join(absolute_dir, relative_path)
    return absolute_file_path


############################################
### Hashing table of the holy grail list ###
############################################


word_set_1 = ws.new_empty_set()

with open(abs_path_fetch("large_texts/holy_grail_words.lst")) as words_list_1:
    for word in words_list_1: 
        ws.add(word_set_1, word)  # Adds every word in the holy grail words list to the word set

printing(word_set_1)      


###########################################
### Hashing table of the 100k sentences ###
###########################################

word_set_2 = ws.new_empty_set()

with open(abs_path_fetch("large_texts/eng_news_100K-sentences_words.lst")) as words_list_2:
    for word in words_list_2: 
        ws.add(word_set_2, word)  # Adds every word in the eng_news words list to the word set

printing(word_set_2)
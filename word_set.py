# A list based hash table implementation for strings.
# Initial bucket size is 10, we the double the bucket size
# when nElements = bucketSize.

size = 0  # global variable, current number of elements


# Returns a new empty set
# The complete function is given and should not be changed.
def new_empty_set():
    """Generate the first set of 10 empty buckets."""

    global size
    size = 0  # Reset the size
    buckets = []
    for i in range(10):
        buckets.append([])
    return buckets


# Adds word to word set if not already added
def add(word_set, word):
    """Computes the hash value of the word and adds it to the set if not already added
    also if the number of words are equal to the amount of buckets available
    will call the rehash function."""

    global size

    h = hash_element(word_set, word)

    if word not in word_set[h]:  # The word is not already in the set
        word_set[h].append(word)
        size += 1

    if size == len(word_set):  # The amount of words in equal to the amount of buckets available
        rehash(word_set)


# Returns current number of elements in set
def count(word_set):
    """Counts the amount of element by adding together the length of every list in the word set."""

    ecount = 0
    for w in word_set:
        ecount += len(w)
    return ecount


# Returns current size of bucket list
def bucket_list_size(word_set):
    """Computes the length of the word set corresponding to the size of the bucket list"""

    return len(word_set)


# Returns a string representation of the set content
def to_string(word_set):
    """Concatenates every element in the lists inside the word set"""

    string = '{'
    for word in word_set:
        for element in word:
            string += ' ' + (str(element))
    return string + ' }'


# Returns True if word in set, otherwise False    
def contains(word_set, word):
    """Computes the hash value of the word and checks the corresponding
    index for the presence of that word"""

    h = hash_element(word_set, word)
    return word in word_set[h]


# Removes word from set if there, does nothing
# if word not in set
def remove(word_set, word):
    """Computes the hash value of the word, and checks the corresponding
    index for the presence of that word and deletes it """

    global size
    h = hash_element(word_set, word)
    if word in word_set[h]:
        del word_set[h][word_set[h].index(word)]
        size -= 1


# Returns the size of the bucket with most elements
def max_bucket_size(word_set):
    """Computes the max between the lengths of every list of words inside the word set"""

    return max([len(bucket) for bucket in word_set])


# Hashing function
# def hash_element(word_set,word):
#     h_val = 0
#     for char in word:
#         h_val += ord(char)
#     return h_val % len(word_set)

def hash_element(word_set, word):
    """Creating an hash value using the DJB2 algoritm"""

    # Source: https://theartincode.stanis.me/008-djb2/
    # Source code: https://gist.github.com/mengzhuo/180cd6be8ba9e2743753

    # The word is passed into the hash_element and the function will return an unsigned int.
    # hash variable is initialized and set to 5381. This is just the value used by the djb2 algoritm.
    # The actual hash function for each char is build looping thruought every character of the word,
    #  taking the value of the hash varivable and shifting it left 5 binary bits and add hash value to that,
    # then adding the ascii value of every single character of the word.
    # The final hash value is computed doing the modulus by the actual size of buckets of the AND operation 
    # between the hash variable and "-1" (two-complement binary 32bits is 0xFFFFFFFF in hexadecimal).

    hash_value = 5381
    for x in word:
        hash_value = ((hash_value << 5) + hash_value) + ord(x)
    return (hash_value & 0xFFFFFFFF) % len(word_set)


# Rehashing function
def rehash(word_set):
    """Rehashes the hash table fist appending every word to a temporary list called 'rehash_temp' then
    empties the word set and doubles it in size, only to call the add function afterwards to add again
    every word stored in the 'rehash_temp' list """

    global size
    rehash_temp = []
    for word in word_set:  # Creating temporary list
        for element in word:
            rehash_temp.append(element)

    for i in range(len(word_set)):  # Emptying the word set and appending the same amount of empty lists
        word_set[i] = []  # doubling the size of the empty buckets
        word_set.append([])

    size = 0
    for element in rehash_temp:  # Adding every word again to the new empty buckets
        add(word_set, element)

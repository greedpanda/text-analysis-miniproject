# A binary search based dictionary implementation
# only using list of length 4.

# Each node is a list of length four where positions
# 0 = key, 1 = value, 2 = left-child, 3 = right-child


# Creates and returns the root to a new empty table.
# The complete function is given and should not be changed.
def new_empty_root():
    """Generate an empty root for a new table."""

    return [None, None, None, None]


# Add a new key-value pair to table if the key doesn't already exist.
# Update value if already key exists in the table.
def add(root, key, value):
    """Add a new key-value pair to a table. If the key already exists, the value for the key is updated."""

    # There are 4 options:
    # - The root has no value yet, because the tree is new
    # - The key is equal to the key value in the current node, so we update it
    # - The key comes before the current node in alphabetical order
    # - The key comes after the current node in alphabetical order

    # Furthermore, we are not sure what the data type of keys will be. In case it is a string, we want to
    # have a lower case version of it to do comparisons with. This is because in ascii, capital letters have a lower
    # value then lower case letters. But in our comparison we don't want to make a difference between lower
    # and upper case for alphabetical order.

    # Create the two variables to compare with. Lower case version if it's a string.
    key_compare = key.lower() if isinstance(key, str) else key
    root_key_compare = root[0].lower() if isinstance(root[0], str) else root[0]

    if root[0] is None:  # It is a new empty tree, so we initialize the root
        root[0] = key
        root[1] = value

    elif root_key_compare == key_compare:  # Update the value
        root[1] = value

    elif key_compare < root_key_compare:  # The key comes before the key of the current node
        if root[2]:  # If it has a left child node
            add(root[2], key, value)  # We move one to the left (recursion)
        else:  # If there is no node, then here is where we should insert
            root[2] = [key, value, None, None]

    elif key_compare > root_key_compare:  # The key comes after the key of the current node
        if root[3]:  # If it has a right child node
            add(root[3], key, value)  # We move one to the right (recursion)
        else:  # If there is no node, then here is where we should insert
            root[3] = [key, value, None, None]


# Returns a string representation of the table content.
# That is, all key-value pairs
def to_string(node):
    """Returns a string representation of the table content (all key-value pairs)."""

    all_pairs = get_all_pairs(node)
    output = "{ "
    for pair in all_pairs:
        output += str(pair) + " "  # Pair is a tuple, so we convert them to a string
    output += " }"
    return output


# Returns the value for the given key. Returns None if key doesn't exists.
def get(node, key):
    """Returns the value for the given key. Returns None if key doesn't exists."""

    # Create the two variables to compare with. Lower case version if it's a string.
    key_compare = key.lower() if isinstance(key, str) else key
    root_key_compare = node[0].lower() if isinstance(node[0], str) else node[0]

    value = None

    if not node[0]:  # The BST hasn't been initialized yet, the root is None
        return None

    elif node[0] == key_compare:  # Fount it
        return node[1]

    # If the key is lower, and a left node exists, go there
    elif key_compare < root_key_compare and node[2]:
        value = get(node[2], key)

    # If the key is higher, and a right node exists, go there
    elif key_compare > root_key_compare and node[3]:
        value = get(node[3], key)

    return value


# Returns the maximum depth (an integer) of the tree.
# That is, the length of longest root-to-leaf path.
def max_depth(node):
    """Returns the length of the longest root-to-leaf path (an integer)."""

    # The method in this article was used and edited to fit our application:
    # https://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/

    if not node[0]:  # This will happen if the root doesn't exist
        return 0

    left_depth = 0
    right_depth = 0

    if node[2]:
        left_depth = max_depth(node[2])  # Compute the depth of the branch to the left

    if node[3]:
        right_depth = max_depth(node[3])

    return max(left_depth, right_depth) + 1  # return the highest one and add one for the current node


# Returns the number og key-value pairs currently stored in the table
def count(node):
    """Returns the number of key-value pairs in the table."""

    # We could also call the get_all_pairs() function and return the length of the list that this functions
    # gives us, but this is way less memory efficient since it stores all the pairs in a list first. This
    # function only uses a counter variable.

    if not node[0]:  # This will happen if the root doesn't exist
        return 0

    counter = 1  # Start at 1 to include the current node

    if node[2]:  # There is a left child node
        counter += count(node[2])  # So we count it and add it to the total

    if node[3]:  # There is a right child node
        counter += count(node[3])  # So we count it and add it to the total

    return counter


# Returns a list of all key-value pairs as tuples 
# sorted as left-to-right, in-order
def get_all_pairs(root):
    """Returns a list of all key-value pairs in the table, as tuples. Sorted as left-to-right, in order."""

    all_pairs = []

    if root[2]:  # Go to the left child node if this exists, and repeat (recursion)
        all_pairs.extend(get_all_pairs(root[2]))

    all_pairs.append((root[0], root[1]))  # Add the current node

    if root[3]:  # Go to the right child node if this exists, and repeat (recursion)
        all_pairs.extend(get_all_pairs(root[3]))

    return all_pairs


def increase(node, key, value=1):
    """Increase the value of a key by the supplied value (if the key exists) (Default increase by 1)."""

    # Create the two variables to compare with. Lower case version if it's a string.
    key_compare = key.lower() if isinstance(key, str) else key
    root_key_compare = node[0].lower() if isinstance(node[0], str) else node[0]

    if not node[0]:  # The BST hasn't been initialized yet, the root is None
        return

    if node[0] == key:
        node[1] += value

    # If the key is lower, and a left node exists, go there
    elif key_compare < root_key_compare and node[2]:
        increase(node[2], key)

    # If the key is higher, and a right node exists, go there
    elif key_compare > root_key_compare and node[3]:
        increase(node[3], key)


def add_or_increase(node, key, value=1):
    """This function is written as a combination between the add() function and the increase() function. This function
    will increase the given key with value (default is 1) in the BST if it exists. If it doesn't exist, it will
    initialize the key with value. This option allows us to only need travel through the BST once, instead of first
    checking if a key exists with get() to see if it needs to be initialized or increased, which will ultimately result
    in 2 travels across the BST."""

    # Create the two variables to compare with. Lower case version if it's a string.
    key_compare = key.lower() if isinstance(key, str) else key
    root_key_compare = node[0].lower() if isinstance(node[0], str) else node[0]

    if not node[0]:  # It is a new empty tree, so we initialize the root
        node[0] = key
        node[1] = value

    elif root_key_compare == key_compare:  # Increase the value
        node[1] += value

    elif key_compare < root_key_compare:  # The key comes before the key of the current node

        if node[2]:  # If it has a left child node
            add_or_increase(node[2], key, value=value)  # We move one to the left (recursion)
        else:  # If there is no node, then here is where we should insert
            node[2] = [key, value, None, None]

    elif key_compare > root_key_compare:  # The key comes after the key of the current node

        if node[3]:  # If it has a right child node
            add_or_increase(node[3], key, value)  # We move one to the right (recursion)
        else:  # If there is no node, then here is where we should insert
            node[3] = [key, value, None, None]

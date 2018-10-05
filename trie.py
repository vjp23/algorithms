from functools import reduce

# Implementation of a Trie data structure for fast word completion


class Trie(object):
    """A Trie node object along with its children.
    
    The Trie data stucture decomposes words into their consituent characters, with each node in the resulting
    tree corresponding to a character. Traversing the tree allow for rapid cword construction based on words
    previously observed by the tree.

    Attributes:
        children: A dictionary keyed by characters and pointing to Trie objects which are children nodes to this node.
        full_word: A boolean indicating whether a word ends at this node. Does not necessarily imply a leaf node.
    """

    def __init__(self, dictionary=None, split_char=None):
        """Initializes the Trie object. 

        No children are added by default, and the full_word indicator is False. If a
        dictionary is specified as a list of strings or as a single long string, then each string will be added.

        Args:
            dictionary: A list containing one or more strings- if one long string, use split_char to split it
            split_char: The string on which to split the dictionary string into strings to add to the tree
        """
        # Use a dictionary for children for constant-time lookups
        self.children = {}
        # Set a flag for indicating that this node marks the end of a complete word
        self.full_word = False
        # Check whether a dictionary was specified
        if dictionary is not None:
            # If the dictionary was entered as a single string, wrap it into a list
            if isinstance(dictionary, str):
                dictionary = [dictionary]
            # Make the dictionary a set to eliminate duplicate words and for later set operations
            dictionary = set(dictionary)
            # Check whether to split the dictionary
            if split_char is not None:
                # Split each sentence in the dictionary, then form a union with the rest of the dictionary set
                # See the get_completions method for more on how this works
                dictionary = reduce(lambda a, b: a | b, [set(sen.split(split_char)) for sen in dictionary])
            # Finally, iterate over the dictionary, adding each word in the set to this Trie node
            for word in dictionary:
                self.insert(word)

    def branch(self, char):
        """Adds a new child node as a new Trie object.
         
         The child node will be keyed as char in the children dictionary.

        Args:
            char: The character used to reference the child node to add
        """
        self.children[char] = Trie()

    def insert(self, word):
        """Insert a new word into this Trie object, treating this as the root node.
        
        Args:
            word: A single string to add to the Trie
        """
        # Begin by setting the node variable to the root node (this Trie object)
        node = self
        for char in word:
            # Iterate through each letter in the word, checking whether it's a child of the current node
            if char not in node.children:
                # If it is not a child already, then add it
                node.branch(char)
            # Now move onto the the child node containing this letter before advancing to the next letter
            node = node.children[char]
        # At the end of this word, set the current node's full_word flag to True to indicate that a word ends here
        node.full_word = True

    def get_completions(self, prefix):
        """Returns a set of all completions of the given prefix.

        Extracts all suffixes of a given prefix, starting from this node, then appends them to the prefix and returns
        
        Args:
            prefix: A string, a prefix for which to search the tree and find suffixes
        
        Returns:
            A set of copmleted words found following the input prefix
        """
        # Define the suffixes as a set to ensure uniqueness among the elements
        suffixes = set()
        # Check whether the current node is a full word; if so, then add it to the set
        if self.full_word:
            suffixes.add(prefix)
        if not self.children:
            # This node has no children- it is a leaf node. Return the suffix set. This is our base case.
            return suffixes
        # If this node does have children, then we need to recursively dig down to the leaf nodes, getting all of the
        # full words between here and those leaves, as well as those leaves themselves. We'll use the reduce() function
        # to continuously apply the set union operator | to the results obtained thus far and the next recursion's
        # results. Then, we'll take the union of our recursive results and the suffix found above (if any).
        return reduce(lambda a, b: a | b, [node.get_completions(prefix + char)
                                           for (char, node) in self.children.items()]) | suffixes

    def complete(self, prefix, n=3):
        """Find autocompletions for a prefix.

        Given an input string prefix, find the suffixes which exist in the tree, add the prefix, and return the list.
        Only returns words which were previously explicitly added to the dictionary as distinct words.

        Args:
            prefix: A string for which to find n full words which begin with the prefix
            n: The number of completions to return- list is truncated arbitrarily
        
        Returns:
            The n complete words in the tree which begin with prefix
        """
        # Before doing anything, handle the edge case of the empty string as an input. We don't have any meangingful
        # guidance here, so return the empty set. We cannot complete a word with no prefix!
        if prefix == '':
            return []
        # Set the node
        node = self
        # Get to the end of the prefix in the tree by traversing down the tree
        for char in prefix:
            if char not in node.children:
                # The next character is not a child of this node; the prefix is not in the tree. Return the empty list
                return []
            # Set the node to the child node with this character
            node = node.children[char]
        # Get all possible completions starting from this node, with this prefix
        completions = list(node.get_completions(prefix))
        # Return the first n entries of the list
        return completions[:n]

    def check_for(self, word):
        """Checks whether the word was entered into the tree  as a full word by searching for it.

        Args:
            word: A single string for which to check the tree
        Returns:
            Boolean value indicating whether word was entered into the tree as a complete word.
        """
        # Initialize the node variable
        node = self
        # Iterate over each letter and check whether it's a child node
        for char in word:
            if char not in node.children:
                # This character is not in the list of child nodes- the word is not in the tree
                return False
            # Update the node
            node = node.children[char]
        # After searching, we see that the entry is in the tree. Determine whether it was entered as a full word
        return node.full_word

if __name__ == '__main__':
    # Load in the Origin of Species text as a dictionary
    with open('origin_of_species.txt', 'r') as text_file:
        dictionary = text_file.read().replace('\n', ' ').lower()

    # Perform some cleanup preprocessing on the text
    dictionary_clean = dictionary
    punclist = ['.', ',', '-', '—', '—', '(', ')', '[', ']', '"', "'", ';', ':', '?', '!']
    for punc in punclist:
        dictionary_clean = dictionary_clean.replace(punc, ' ')

    # Define a new tree with this dictionary, splitting it all on spaces
    tree = Trie(dictionary_clean, ' ')

    # Try searching for a word known to be in the tree
    if tree.check_for('species'):
        print('The word "species" was found in the tree.')
    else:
        print('The word "species" was not found in the tree.')
    
    # Test out the completions
    print('The first 3 word completions for "natu" are:')
    print(tree.complete('natu', 3))
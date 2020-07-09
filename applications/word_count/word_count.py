def word_count(s):
    """
    Input: This function takes a single string as an argument.
    Output: It returns a dictionary of words and their counts.
    
    Case should be ignored. Output keys must be lowercase.
    Key order in the dictionary doesn't matter.
    Split the strings into words on any whitespace.
    Ignore each of the following characters:
        " : ; , . - + = / \\ | [ ] { } ( ) * ^ &
    """

    # could use defaultdict from NLP lesson ?
    # have stop characters instead of stop words

    cache = {}
    stop_chars = [':', ';', ',', '.', '"', '-', '+', '=', '/',
             '\\', '|', '[', ']', '{', '}', '(', ')', '*', '^', '&']
    
    # replace stop characters
    for i in stop_chars:
        s = s.replace(i, '')

    words = s.lower().split()
    
    for word in words:
        if word in cache:
            cache[word] += 1
        else:
            cache[word] = 1
    return cache


if __name__ == "__main__":
    print(word_count(""))
    print(word_count("Hello"))
    print(word_count('Hello, my cat. And my cat doesn\'t say "hello" back.'))
    print(word_count('This is a test of the emergency broadcast network. This is only a test.'))
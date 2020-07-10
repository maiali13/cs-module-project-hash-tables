# Use frequency analysis to find the key to ciphertext.txt, and then decode it.

# need 2 fxns
# 1st to encode char frequency
# 2nd to decode text


# List of alphabet letters in order of expected frequency, from most to least frequent
frequency_list = ['E', 'T', 'A', 'O', 'H', 'N', 'R', 'I', 'S', 'D', 'L', 'W', 'U',
             'G', 'F', 'B', 'M', 'Y', 'C', 'P', 'K', 'V', 'Q', 'J', 'X', 'Z']


def letter_frequency(words, letters= frequency_list):
    cache = {}
    for char in words:
        if char not in letters:
            continue
        if char not in cache:
            cache[char] = 1
        else:
            cache[char] += 1
    return sorted(cache.items(), key=lambda x: x[1], reverse=True)


def ceasar_salad(words):
    letter_freq = letter_frequency(words)
    # match letters to frequency percentage
    match = {letter_freq[i][0]:frequency_list[i]
                for i in range (len(letter_freq))}
    translate = ''.join(map(lambda x: match[x] if x in match else x, words))
    print(translate)




if __name__ == "__main__":
    # read cyphertext file
    with open('ciphertext.txt') as file:
        ciphertext = file.read()   

    print(ceasar_salad(ciphertext))
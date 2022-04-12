
import re
import random

alphabet = "abcdefghijklmnopqrstuvwxyz"
auto = True # set to False if you want to make the decisions yourself

def main():
    out = []
    with open("/usr/share/dict/words", "r") as words: # get dictionary file, available by default on unix
        s = words.readlines()
    used = ['']*5 # store used characters for each index
    for char in alphabet: # go through alphabet, try to put each char on each index 
        for index in range(5):
            if char in used[index]: # if this character has already appeared at this index, don't check it again
                continue
            rgx = ['']*5 # create regex for each 
            for i in range(5):
                x = stringdiff(alphabet, used[i]) # get characters we haven't checked yet for each index
                rgx[i] = f"[{x}]" if x != "" else "[a-z]" # if we've done them all, we need to allow any character here
            rgx[index] = char # character at the current index must be this one.
            pattern = re.compile('^' + "".join(rgx) + '$')
            m = arrange([pattern.search(x).group(0) for x in s if pattern.search(x)], char) # find matching words in dictionary and order them in some clever way
            if len(m) == 0:
                m, pattern = fuzzify(rgx.copy(), 5, index, char, s) # be less strict about what characters can be where if there are no matches
            if not auto and m != []: # inform user of matching words and context
                print(m)
                print(f"regex used: {pattern.pattern}")
                choice = input("chosen word: ")[:5]
            else:
                if m != []:
                    choice = m[0] #random.choice(m) # naively pick first answer (works pretty well)   
                    out.append(choice)
                else: # it's possible there are no five letter words with this character at this index
                    choice = char * (index+1) +'a'*5 # make regexes not look for this character at this index
            if len(choice) >= 5: # in case of user error
                for i in range(5):
                    used[i] += choice[i]
    print(out, "\n", len(out)) # give answers and how many they are. Always input in order, to possibly have fewer guesses than words found.

def count(str, ch): # count occurences of ch in str
    s = 0
    for c in str:
        if c == ch:
            s += 1
    return s

def arrange(m, ch): # arrange list m by some method, CHANGE this. current character is available if needed
    return m # sorted(m, key = lambda x: count(x, ch), reverse=False)

def stringdiff(string1, string2): # set difference string1 - string2. Used for alphabet subsets
    return "".join([c for c in string1 if c not in string2])

# HINT: Does not try all permutations of allowed characters at indices. Change that?
def fuzzify(rgx, n, index, backup, s): # make more options available. returns found matches and pattern used to find them
    if n == 0: # base case
        ls = ['[a-z]']*5 # all characters allowed at all indices 
        ls[index] = backup # except the one we want to make sure appears here
        pattern = re.compile('^' + "".join(ls) + '$')
        m = [pattern.search(x).group(0) for x in s if pattern.search(x)]
        return arrange(m, backup), pattern
    for i in range(n): # try to allow each index individually to be any character
        if i == index: continue # don't change the relevant character
        ls = rgx.copy() # don't modify outer list
        ls[i] = '[a-z]'
        pattern = re.compile('^' + "".join(ls) + '$')
        m = [pattern.search(x).group(0) for x in s if pattern.search(x)]
        if len(m) > 0: # if there are options
            break
    else: # if loop isn't broken
        return fuzzify(ls, n-1, index, backup, s) # try to make more indices any character
    return arrange(m, backup), pattern 

if __name__ == "__main__":
    main()


#import Tree
#
#verbose = False
#def printV(*args):
#    if verbose:
#        print(*args)
#
## A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
#def CYKParse(words, grammar):
#    T = {}
#    P = {}
#    # Instead of explicitly initializing all P[X, i, k] to 0, store
#    # only non-0 keys, and use this helper function to return 0 as needed.
#    def getP(X, i, k):
#        key = str(X) + '/' + str(i) + '/' + str(k)
#        if key in P:
#            return P[key]
#        else:
#            return 0
#    # Insert lexical categories for each word
#    for i in range(len(words)):
#        for X, p in getGrammarLexicalRules(grammar, words[i]):
#            P[X + '/' + str(i) + '/' + str(i)] = p
#            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
#    printV('P:', P)
#    printV('T:', [str(t)+':'+str(T[t]) for t in T])
#    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
#    for i, j, k in subspans(len(words)):
#        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
#            printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']',
#                    'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
#            PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
#            if PYZ > getP(X, i, k):
#                printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
#                            'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
#                            'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
#                P[X + '/' + str(i) + '/' + str(k)] = PYZ
#                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
#    printV('T:', [str(t)+':'+str(T[t]) for t in T])
#    return T, P
#
## Python uses 0-based indexing, requiring some changes from the book's
## 1-based indexing: i starts at 0 instead of 1
#def subspans(N):
#    for length in range(2, N+1):
#        for i in range(N+1 - length):
#            k = i + length - 1
#            for j in range(i, k):
#                yield i, j, k
#
## These two getXXX functions use yield instead of return so that a single pair can be sent back,
## and since that pair is a tuple, Python permits a friendly 'X, p' syntax
## in the calling routine.
#def getGrammarLexicalRules(grammar, word):
#    for rule in grammar['lexicon']:
#        if rule[1] == word:
#            yield rule[0], rule[2]
#
#def getGrammarSyntaxRules(grammar):
#    rulelist = []
#    for rule in grammar['syntax']:
#        yield rule[0], rule[1], rule[2], rule[3]

import Tree

num=''
verbose = False

def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    for i in range(len(words)):
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
            for grammerrr in getGrammarSyntaxRules(grammar):
                if len(grammerrr)== 4:
                    phase, word, wordd,prob = grammerrr
                    if word ==X or wordd== X:
                        P[phase + '/' + str(i) + '/' + str(i)] = prob
                        T[phase+'/'+str(i) + '/'+str(i)] = Tree.Tree(phase, T[X +'/'+ str(i) +'/'+ str(i)], '', lexiconItem=words[i])
                if len(grammerrr)== 3:
                    phase, word, prob = grammerrr
                    if word ==X:
                        P[phase + '/' + str(i) + '/' + str(i)] = prob
                        T[phase+'/'+str(i) + '/'+str(i)] = Tree.Tree(phase, T[word +'/'+ str(i) +'/'+ str(i)], '', lexiconItem=words[i])
                        
    printV('P:', P)
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    print('\n')
    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first

    
#     for i, j, k in subspans(len(words)):
#         for X, Y, Z, p in getGrammarSyntaxRules(grammar):
# #             printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']',
# #                     'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
#             if Z is not None:
#                 PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
#                 if PYZ > getP(X, i, k) :
#     #                 printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
#     #                             'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
#     #                             'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
# #                     for rule in getGrammarSyntaxRules(grammar):
# #                         P[rule[0] + '/' + str(i) + '/' + str(k)] = PYZ
# #                         T[rule[0] + '/' + str(i) + '/' + str(k)] = Tree.Tree(rule[0], T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
#                     P[X + '/' + str(i) + '/' + str(k)] = PYZ
#                     T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
#             else:
#                 PYZ = getP(Y, i, j) * p
#                 if PYZ > getP(X, i, k) :
#     #                 printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
#     #                             'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
#     #                             'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
# #                     for rule in getGrammarSyntaxRules(grammar):
# #                         P[rule[0] + '/' + str(i) + '/' + str(k)] = PYZ
# #                         T[rule[0] + '/' + str(i) + '/' + str(k)] = Tree.Tree(rule[0], T[Y+'/'+str(i)+'/'+str(j)], None)
#                     P[X + '/' + str(i) + '/' + str(k)] = PYZ
#                     T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], None)

    for i, j, k in subspans(len(words)):
            for wordd  in getGrammarSyntaxRules(grammar):
                if len(wordd) ==4:
    #                 printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']',
    #                          'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
                    PYZ = getP(wordd[1], i, j) * getP(wordd[2], j+1, k) * wordd[3]
                    if PYZ > getP(wordd[0], i, k):
    #                     printV('     inserting from', i,'-',k,' ',X,'->',T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
    #                                 'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
    #                                 'getP(' +  + ',' + str(i) + ',' + str(k) + ')')
                        P[wordd[0] + '/' + str(i) + '/' + str(k)] = PYZ
                        T[wordd[0] + '/' + str(i) + '/' + str(k)] = Tree.Tree(wordd[0], T[wordd[1]+'/'+str(i)+'/'+str(j)], T[wordd[2]+'/'+str(j+1)+'/'+str(k)], lexiconItem=words[i])
            if len(wordd) ==3:
    #                 printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']',
    #                          'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
                    PY = getP(wordd[1], i, j) * wordd[2]
                    if PYZ > getP(wordd[0], i, k):
    #                     printV('     inserting from', i,'-',k,' ',X,'->',T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
    #                                 'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
    #                                 'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
                        P[wordd[0] + '/' + str(i) + '/' + str(k)] = PY
                        T[wordd[0] + '/' + str(i) + '/' + str(k)] = Tree.Tree(wordd[0], T[wordd[1]+'/'+str(i)+'/'+str(j)],'', lexiconItem=words[i])
#     completeSentenceTree = []
#     sentenceTrees = { k: v for k,v in T.items()if k.startswith('S/0') }
#     oo = sorted(sentenceTrees.keys(),reverse = True)[0]
#     completeSentenceTree.append(oo)
#     global num
#     num = max(completeSentenceTree)
    
    
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P


    
# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]

def getGrammarSyntaxRules(grammar):
    rulelist = []
    for rule in grammar['syntax']:
        if len(rule)==4:
            added1 = True
            yield rule[0], rule[1], rule[2], rule[3]
        if len(rule)==3:
            yield rule[0], rule[1], rule[2]

# 'Grammar' here is used to include both the syntax part and the lexicon part.

# E0 from AIMA, ps. 834.  Note that some syntax rules were added or modified
# to shoehorn the rules into Chomsky Normal Form.
def getGrammarE0():
    return {
        'syntax' : [
            ['S', 'NP', 'VP', 0.9 * 0.45 * 0.6],
            ['S', 'Pronoun', 'VP', 0.9 * 0.25 * 0.6],
            ['S', 'Name', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'Noun', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'NP', 'Verb', 0.9 * 0.45 * 0.4],
            ['S', 'Pronoun', 'Verb', 0.9 * 0.25 * 0.4],
            ['S', 'Name', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'Noun', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'S', 'Conj+S', 0.1],
            ['Conj+S', 'Conj', 'S', 1.0],
            ['NP', 'Article', 'Noun', 0.25],
            ['NP', 'Article+Adjs', 'Noun', 0.15],
            ['NP', 'Article+Adjective', 'Noun', 0.05],
            ['NP', 'Digit', 'Digit', 0.15],
            ['NP', 'NP', 'PP', 0.2],
            ['NP', 'NP', 'RelClause', 0.15],
            ['NP', 'NP', 'Conj+NP', 0.05],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Conj+NP', 'Conj', 'NP', 1.0],
            ['VP', 'VP', 'NP', 0.6 * 0.55],
            ['VP', 'VP', 'Adjective', 0.6 * 0.1],
            ['VP', 'VP', 'PP', 0.6 * 0.2],
            ['VP', 'VP', 'Adverb', 0.6 * 0.15],
            ['VP', 'Verb', 'NP', 0.4 * 0.55],
            ['VP', 'Verb', 'Adjective', 0.4 * 0.1],
            ['VP', 'Verb', 'PP', 0.4 * 0.2],
            ['VP', 'Verb', 'Adverb', 0.4 * 0.15],
            ['Adjs', 'Adjective', 'Adjs', 0.8],
            ['PP', 'Prep', 'NP', 0.65],
            ['PP', 'Prep', 'Pronoun', 0.2],
            ['PP', 'Prep', 'Name', 0.1],
            ['PP', 'Prep', 'Noun', 0.05],
            ['RelClause', 'RelPro', 'VP', 0.6],
            ['RelClause', 'RelPro', 'Verb', 0.4]
        ],
        'lexicon' : [
            ['Noun', 'stench', 0.05],
            ['Noun', 'breeze', 0.05],
            ['Noun', 'wumpus', 0.05],
            ['Noun', 'pits', 0.05],
            ['Noun', 'dungeon', 0.05],
            ['Noun', 'frog', 0.05],
            ['Noun', 'balrog', 0.7],
            ['Verb', 'is', 0.1],
            ['Verb', 'feel', 0.1],
            ['Verb', 'smells', 0.1],
            ['Verb', 'stinks', 0.05],
            ['Verb', 'wanders', 0.65],
            ['Adjective', 'right', 0.1],
            ['Adjective', 'dead', 0.05],
            ['Adjective', 'smelly', 0.02],
            ['Adjective', 'breezy', 0.02],
            ['Adjective', 'green', 0.81],
            ['Adverb', 'here', 0.05],
            ['Adverb', 'ahead', 0.05],
            ['Adverb', 'nearby', 0.02],
            ['Adverb', 'below', 0.88],
            ['Pronoun', 'me', 0.1],
            ['Pronoun', 'you', 0.03],
            ['Pronoun', 'I', 0.1],
            ['Pronoun', 'it', 0.1],
            ['Pronoun', 'she', 0.67],
            ['RelPro', 'that', 0.4],
            ['RelPro', 'which', 0.15],
            ['RelPro', 'who', 0.2],
            ['RelPro', 'whom', 0.02],
            ['RelPro', 'whoever', 0.23],
            ['Name', 'Ali', 0.01],
            ['Name', 'Bo', 0.01],
            ['Name', 'Boston', 0.01],
            ['Name', 'Marios', 0.97],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05],
            ['Prep', 'to', 0.2],
            ['Prep', 'in', 0.1],
            ['Prep', 'on', 0.05],
            ['Prep', 'near', 0.10],
            ['Prep', 'alongside', 0.55],
            ['Conj', 'and', 0.5],
            ['Conj', 'or', 0.1],
            ['Conj', 'but', 0.2],
            ['Conj', 'yet', 0.2],
            ['Digit', '0', 0.1],
            ['Digit', '1', 0.1],
            ['Digit', '2', 0.1],
            ['Digit', '3', 0.1],
            ['Digit', '4', 0.1],
            ['Digit', '5', 0.1],
            ['Digit', '6', 0.1],
            ['Digit', '7', 0.1],
            ['Digit', '8', 0.1],
            ['Digit', '9', 0.1]
        ]
    }

# To experiment with the 'garden path' sentence 'the old man the boat'
def getGrammarGardenPath():
    return {
        'syntax' : [
            ['S', 'NP', 'VP', 0.25],
            ['S', 'Noun', 'VP', 0.25],
            ['S', 'NP', 'Verb', 0.25],
            ['S', 'Noun', 'Verb', 0.25],
            ['NP', 'Article', 'Noun', 0.4],
            ['NP', 'Article+Adjs', 'Noun', 0.2],
            ['NP', 'Article+Adjective', 'Noun', 0.4],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Adjs', 'Adjective', 'Adjs', 0.8],
            ['VP', 'Verb', 'NP', 1.0],
        ],
        'lexicon' : [
            ['Noun', 'man', 0.5],
            ['Noun', 'old', 0.1],
            ['Noun', 'boat', 0.4],
            ['Verb', 'man', 0.1],
            ['Verb', 'sail', 0.1],
            ['Verb', 'think', 0.8],
            ['Adjective', 'old', 0.1],
            ['Adjective', 'young', 0.1],
            ['Adjective', 'red', 0.8],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05]
        ]
    }

# To experiment with 'I saw a man with my telescope'
def getGrammarTelescope():
    return {
        'syntax' : [
            ['S', 'Pronoun', 'VP', 1],
            ['VP', 'Verb', 'NP', 0.6],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.4],
            ['NP', 'Article', 'Noun', 0.3],
            ['NP', 'Adjective', 'Noun', 0.3],
            ['NP', 'NP', 'AdjectivePhrase', 0.4],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 1.0],
            ['AdverbPhrase', 'Preposition', 'NP', 1.0],
        ],
        'lexicon' : [
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.8],
            ['Noun', 'telescope', 0.2],
            ['Verb', 'saw', 1.0],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Preposition', 'with', 1.0],
         ]
    }

# Sample sentences:
# Hi, I am Peter. I am Peter. Hi, my name is Peter. My name is Peter.
# What is the temperature in Irvine? What is the temperature in Irvine now?
# What is the temperature in Irvine tomorrow?
#
def getGrammarWeather():
    return {
        'syntax' : [
            ['S', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.25],
            ['S', 'Pronoun', 'VP', 0.25],
            ['S', 'WQuestion', 'VP', 0.25],
            ['VP', 'Verb', 'NP', 0.4],
            ['VP', 'Verb', 'Name', 0.2],
            ['VP', 'Verb', 'NP', 0.1],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['NP', 'Article', 'Noun', 0.5],
            ['NP', 'Adjective', 'Noun', 0.5],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.2],
            ['NP+AdverbPhrase', 'Noun', 'AdverbPhrase', 0.2],
            ['NP+AdverbPhrase', 'Noun', 'Adverb', 0.2],
            ['NP+AdverbPhrase', 'NP', 'Adverb', 0.15],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.05],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'Noun', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'Noun', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP', 0.05],
            ['AdverbPhrase', 'Preposition', 'NP', 0.2],
            ['AdverbPhrase', 'Preposition', 'Name', 0.2],
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],
        ],
        'lexicon' : [
            ['Adjective', 'dead', 0.05],
            ['Noun', 'wumpus', 0.05],
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['WQuestion', 'how', 0.5],
            ['Verb', 'am', 0.5],
            ['Verb', 'is', 0.5],
            ['Name', 'Peter', 0.1],
            ['Name', 'Sue', 0.1],
            ['Name', 'Irvine', 0.8],
            ['Pronoun', 'I', 1.0],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.6],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.3],
            ['Adverb', 'tomorrow', 0.3],
            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.5],
            ['Noun', 'Tustin', 0.2],
            ['Noun', 'Pasadena', 0.2],
            ['Adverb', 'yesterday', 0.3],
            ['WQuestion', 'Will', 0.25],
            ['Adverb', 'hotter', 0.3],
            ['Preposition', 'than', 0.5],
            ['Verb', 'be', 0.5],

         ]
    }

# Unit testing code
if __name__ == '__main__':
    verbose = True
    #CYKParse(['the', 'wumpus', 'is', 'dead'], getGrammarE0())
    #CYKParse(['the', 'old', 'man', 'the', 'boat'], getGrammarGardenPath())
    #CYKParse(['I', 'saw', 'a', 'man', 'with', 'my', 'telescope'], getGrammarTelescope())
    #CYKParse(['my', 'name', 'is', 'Peter'], getGrammarWeather())
    #CYKParse(['hi', 'I', 'am', 'Peter'], getGrammarWeather())
    #CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine'], getGrammarWeather())
    #CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine', 'now'], getGrammarWeather())
    #CYKParse(['what', 'is', 'the', 'temperature', 'now', 'in', 'Irvine'], getGrammarWeather())
    #CYKParse(['what', 'is', 'now', 'the', 'temperature', 'in', 'Irvine'], getGrammarWeather())
    CYKParse(['let', 'me', 'know', 'Tustin', 'today', 'tempreature'], getGrammarWeather())


# Hi, I am Peter. I am Peter. Hi, my name is Peter. My name is Peter.
# What is the temperature in Irvine? What is the temperature in Irvine now?
# What is the temperature in Irvine tomorrow? 

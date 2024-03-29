"""
The core chunk of code designed to handle and process our designated data
for us.
"""

from __future__ import division, with_statement
import os, re, string
from nltk import word_tokenize, pos_tag
from collections import defaultdict

from porter import PorterStemmer


# Our stemmer, whips words into shape for eval
PORTER = PorterStemmer()

# DATA DIRECTORIES
TRAINDIR = 'task05-TRAIN/train/'
TRIALDIR = 'trial/'
TESTDIR = 'trial/'

# FILE REGEXES
DATA_FILE_REGEX = '(C|H|I|J)-\d+.txt.final'
DATA_IDENT_REGEX = '(C|H|I|J)-\d+'
STEM_KEY_FILE_REGEX = \
    '(trial|test|train).(author|reader|combined).stem.final'
LEM_KEY_FILE_REGEX = '(trial|test|train).(author|reader|combined).final'

# GLOBAL DATA
KEY_TYPES = ['authorkey', 'readerkey', 'combinedkey']


def filenameToIdent(filename):
  return re.match(DATA_IDENT_REGEX, filename).group()

def walkMatchedFiles(direct, fileRegex):
  """
  Walks directory, returns all files that are data files
  """
  for root,dirs,files in os.walk(direct):
    for f in files:
      if re.match(fileRegex, f):
        yield direct + f, f

def walkTrainDataLine():
  """
  Walks training data directory, returning each line of each data file, one
  line at a time.
  """
  for path,f,doc in walkTrainDataDoc():
    for line in doc:
      yield (path, f, line.strip())

def walkTrainDataDoc():
  for path,f in walkMatchedFiles(TRAINDIR, DATA_FILE_REGEX):
    with open(path) as opened:
      yield (path, f, opened.read())

def walkTrialDataDoc():
  for path,f in walkMatchedFiles(TRIALDIR, DATA_FILE_REGEX):
    #print path, f
    with open(path) as opened:
      yield (path, f, opened.read())

def processKeyFile(f):
  """
  Takes filename, returns dictionary with answers for every document,
  indexed by document name

  Each line is has a key and a set of answers. They are separated by a ':',
  e.g., [key] : [answers]. We simply walk through line-by-line and split
  as such.
  """
  key = {}
  with open(f) as opened:
    for line in opened.readlines():
      docname,answers = line.split(':')
      docname = docname.strip()
      answers = answers.split(',')
      answers = map(string.strip, answers)
      key[docname] = answers

  return key

def trainingKeys(format='stemmed'):
  """
  Obtains author, reader, and combined solutions for each document in
  training set.

  Solutions are formatted as a dictionary: keys are filenames, values are
  the keywords for that file.
  """

  # Make sure we're getting the correct format of key -- stemmed or
  # lemmatized?
  if format == 'stemmed':
    regex = STEM_KEY_FILE_REGEX
  elif format == 'lemmatized':
    regex = LEM_KEY_FILE_REGEX
  else:
    raise ValueError("trainingKeys() doesn't recognize that type of key!")

  keylist = []
  for path,f in walkMatchedFiles(TRAINDIR, regex):
    annotator = re.search('(author|reader|combined)', f).group()
    key = processKeyFile(path)

    keylist.append((annotator, path, f, key))

  return keylist

def keyHist():
  """
  Takes the training keys for author, reader, and combined, outputs
  a key histogram based on the answers.
  """

  keylist = trainingKeys()

  hist = defaultdict(lambda:0)
  docs = set()  # set of documents we've consumed; useful for bookkeeping
  for annotator,path,f,key in keylist:
    for docname,answers in key.items():
      docs.add(docname)
      for answer in answers:
        hist[answer] += 1

  return hist, docs

def docWordMap(document):
  """
  Creates a 1-1 bijective pairing between every word and its lemmatized
  version in a document; takes raw text of document, returns two lists
  of equal length, one containing all the words in the document, the other
  containing the lemmatized versions of each of those words.
  """
  words = word_tokenize(document)
  stemmed = [stemWord(word) for word in words]

  return words, stemmed

def findAnswInWordMap(answ, stemdoc):
  """
  Takes the stemmed answer, the document, and the stemmed wordmap of the
  document and looks through them to find the indices where the term
  appears

  NOTE: DOES NOT HANDLE OVERLAPPING PATTERNS
  """
  answwords = word_tokenize(answ)
  len_stemdoc = len(stemdoc)
  len_answ = len(answwords)
  i = 0  # pos in stemdoc
  j = 0  # pos in answwords
  while True:
    if i >= len_stemdoc:
      break

    if stemdoc[i] == answwords[j]:
      # Walk through both as long as they match
      while j < len_answ and i < len_stemdoc and stemdoc[i] == answwords[j]:
        i += 1
        j += 1

      # If it's a complete match, yield match indices, else start matching
      # over again
      if j == len_answ:
        yield (i - len_answ, i)
        j = 0
      else:
        i = i - j + 1
        j = 0
    else:
      i += 1

def wordmapcmp_xcoord(x,y):
  # NOTE: ASSUMES TERMS DO NOT OVERLAP!
  if x[0] != y[0]:
    return x[0] - y[0]
  else:
    return y[1] - x[1]

def wordmapcmp_ycoord(x,y):
  # NOTE: ASSUMES TERMS DO NOT OVERLAP!
  if x[1] != y[1]:
    return x[1] - y[1]
  else:
    return y[0] - x[0]

def stemWord(word):
  """
  Stems a single word using the Porter stemmer.
  """
  output = PORTER.stem(word, 0, len(word) - 1)
  return output

def stemString(string):
  """
  Stems a whole string using the Porter stemmer.
  """
  output = ''
  word = ''

  for c in string:
    if c.isalpha():
      word += c.lower()
    else:
      if word:
        output += stemWord(word)
        word = ''
      output += c.lower()

  if word:
    output += stemWord(word)

  return output

def writeResults(predictionlist):
  with open('results.stm', 'w') as w:
    for docname,wrdlist in predictionlist:
      prediction = '%s : %s\n' % (docname, ','.join(wrdlist)[:-1])
      w.write(prediction)

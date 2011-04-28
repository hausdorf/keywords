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
  for annotator,path,f,key in keylist:
    for docname,answers in key.items():
      for answer in answers:
        hist[answer] += 1

  return hist

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
    for p in predictionlist:
      w.write(p + '\n')

"""
The core chunk of code designed to handle and process our designated data
for us.
"""

from __future__ import division, with_statement
import os, re, string


# DATA DIRECTORIES
TRAINDIR = 'task05-TRAIN/train/'
TRIALDIR = 'trial/'
TESTDIR = 'trial/'

# FILE REGEXES
DATA_FILE_REGEX = '(C|H|I|J)-\d+.txt.final'
STEM_KEY_FILE_REGEX = \
    '(trial|test|train).(author|reader|combined).stem.final'
LEM_KEY_FILE_REGEX = '(trial|test|train).(author|reader|combined).final'


def walkMatchedFiles(direct, fileRegex):
  """
  Walks directory, returns all files that are data files
  """
  for root,dirs,files in os.walk(TRAINDIR):
    for f in files:
      if re.match(fileRegex, f):
        yield direct + f

def walkTrainData():
  """
  Walks training data directory, returning each line of each data file, one
  line at a time.
  """
  for f in walkMatchedFiles(TRAINDIR, DATA_FILE_REGEX):
    with open(f) as opened:
      for line in opened.readlines():
        yield (f, line.strip())

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
    raise "trainingKeys() doesn't recognize that type of key!"

  keylist = []
  for f in walkMatchedFiles(TRAINDIR, regex):
    annotator = re.search('(author|reader|combined)', f).group()
    key = processKeyFile(f)

    keylist.append((annotator, f, key))

  return keylist

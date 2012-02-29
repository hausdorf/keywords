"""
Core logic for learning to identify keywords.
"""

from collections import defaultdict


class NaiveDictLookup:
  def __init__(self, authorkey, readerkey, combinedkey, hist='reader'):
    self.authorkey = authorkey
    self.readerkey = readerkey
    self.combinedkey = combinedkey
    self.keymap = {'reader': self.readerkey, 'author': self.authorkey,
        'combined': self.combinedkey}

    # Halt if invalid type of histogram
    if hist not in self.keymap:
      raise ValueError('NaiveDictLookup has failed to initialize because' \
          + 'your choice of histogram type is invalid')

    # Assemble histogram
    self.anshist = defaultdict(lambda:0)
    for docname,answers in self.authorkey.items():
      for a in answers:
        self.anshist[a] += 1

  def keywords(text):
    return


if __name__ == '__main__':
  print stemString('cows are stemmed')

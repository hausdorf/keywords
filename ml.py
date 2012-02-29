"""
Core logic for learning to identify keywords.
"""

from porter import PorterStemmer


# Our stemmer, whips words into shape for eval
PORTER = PorterStemmer()


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


if __name__ == '__main__':
  print stemString('cows are stemmed')

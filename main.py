"""
Handles main control logic for our keyword extractor. Addresses SemEval 2010
task found at[1]. Data is found at[2].

(c) 2012 Alex Clemmer

[1] https://docs.google.com/Doc?id=ddshp584_46gqkkjng4
[2] The data are found at number 5 on the list, titled "Automatic Keyphrase
    Extraction...". The URL is:
    http://semeval2.fbk.eu/semeval2.php?location=data
"""
import sys

import data, ml


def main():
  authorkey,combinedkey,readerkey = data.trainingKeys()

  i = 0
  for path,f,doc in data.walkTrainDataDoc():
    print doc

    print i
    i += 1


if __name__ == '__main__':
  main()

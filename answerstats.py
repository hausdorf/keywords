"""
A series of experiments dealing with the answers.
"""

from collections import defaultdict
import matplotlib.pyplot as plot
from nltk import FreqDist
import data


def answerhist():
  trainingkeylist = map(lambda (x,y,key): key, data.trainingKeys())

  hist = []
  for key in trainingkeylist:
    for docname,answers in key.items():
      for a in answers:
        hist.append(filter(lambda x: ord(x) < 128, a))

  return hist

def _expt0_answerhist():
  hist = answerhist()

  fdist = FreqDist(hist)
  fdist.plot(50)

def main():
  _expt0_answerhist()


if __name__ == '__main__':
  main()

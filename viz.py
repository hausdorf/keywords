# TODO TODO TODO
# THERE ARE MANY THINGS TODO!
# * We want all three types of key (reader, author, combined) to show up in
#   the same document! They currently all show up in different docs
# * We want to handle overlapping tags! Currently we just hope there are
#   no overlapping tags (and this generally seems to be true, fortunately


import re, sys, string
from itertools import groupby

import data


# DIRECTORIES: where we store our marked-up HTML training stuff

DIRECTORY = 'trainingviz/'

# REGEXES
WORD_JOIN_BASIS = '[%s \n\r\c]+' % re.escape(string.punctuation)


# HTML BASIS: strings we use to produce a document

HEADER = """
<html>
<head>
<title>%s</title>
</head>

<body>
<h1>%s</h1>
"""

FOOTER = """
</body>
</html>
"""


# CONFIG: variables that define how our HTML stuff looks

KEYCOLOR = {'author': 'red', 'reader': 'blue', 'combined': 'green'}


def annotateTrainingDoc(filename, document, docwords, kwindices, keytype):
  """
  Takes a the word_tokenized document, annotates according to the indices
  of the keywords, and then writes out.
  """
  #for ind in kwindices:
    #print docwords[ind[0]:ind[1]]

  doclower = document.lower()  # must be lower case to match our lem'd words
  i_doc = 0
  i_kwi = 0
  buf = ''
  #print len(docwords), len(kwindices),
  #print kwindices[i_kwi][0],
  #print kwindices[i_kwi][1]
  phrase = ' '.join(docwords[kwindices[i_kwi][0]:kwindices[i_kwi][1]])

  while i_doc < len(document):
    matched = re.match(phrase, doclower[i_doc:])
    # move to next char if no match
    if matched:
      match = matched.group(0)
      #print 'MATCH', i_doc, i_kwi, phrase

      # stick `<font>` tags around it
      buf += '<font size=5px color="%s"><b>%s</b></font>' % \
          (KEYCOLOR[keytype[:-3]], document[i_doc:i_doc+len(match)])
      i_doc += len(match)
      i_kwi += 1
      if i_kwi >= len(kwindices):
        break

      phrase = ' '.join(docwords[kwindices[i_kwi][0]:kwindices[i_kwi][1]])


      """
      print buf
      print
      print
      print
      if i_doc > 900:
        print i_doc, i_kwi, phrase
        sys.exit()
      """
    else:
      buf += document[i_doc]
      i_doc += 1

  while i_doc < len(document):
    buf += document[i_doc]
    i_doc += 1


  return buf


def assemblePage(filepath, filename, document, keydict):
  """
  Assembles a single training document as marked-up HTML
  """

  ident = data.filenameToIdent(filename)
  print ident,
  # NOTE: THIS ALL ASSUMES YOU'RE USING STEMMED ANSWERS
  # TODO: THIS SHOULD NOT ASSUME YOU'RE USING STEMMED ANSWERS!
  words, stemmed = data.docWordMap(document)

  answlist = []
  for t in data.KEY_TYPES:
    print t,
    docansw = keydict[t][3][ident]
    answlist.append(docansw)
    for answ in docansw:
      indices = [(i,j) for i,j in data.findAnswInWordMap(answ, stemmed)]
      indices.sort(cmp=data.wordmapcmp_xcoord)

      if len(indices) == 0:
        continue

      """
      q = [(1,4), (2,3), (1,2), (3,4)]
      q.sort(cmp=data.wordmapcmp_xcoord)
      print q
      for i in indices:
        print i
      """

      # Do stuff here
      document = annotateTrainingDoc(filename, document, words,
          indices, t)

    document = re.sub('\n\n', '<p><p>\n', document)
    document = re.sub('\n', '<br />\n', document)

    page = ''  # Will contain out entire output page
    page += HEADER % (filename, filename)
    page += str(answlist)
    page += '<p><p>'
    page += document
    page += FOOTER

    f = open(DIRECTORY + ident + '_' + t + '.html', 'w')
    f.write(page)
    f.close()

  print


  """
  page += str(answlist)
  page += '<p><p>'
  page += document
  page += FOOTER
  print page
  """

  """
  for name,key in keydict.items():

    page = ''  # Will contain out entire output page
    page += HEADER % (filename, filename)

    # Do stuff here
    document,identifier = annotateTrainingDoc(filename, document, key, name)
    print identifier

    page += document

    page += FOOTER

    f = open(DIRECTORY + identifier + '.html', 'w')
    f.write(document)
    f.close()
  """

def assembleAllPages():
  """
  Assembles all training documents as marked-up HTML
  """

  authorkey,combinedkey,readerkey = data.trainingKeys()
  keydict = {'authorkey': authorkey, 'combinedkey': combinedkey,
      'readerkey': readerkey}

  for path,f,doc in data.walkTrainDataDoc():
    page = assemblePage(path, f, doc, keydict)


if __name__ == '__main__':
  assembleAllPages()


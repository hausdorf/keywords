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


def openTags(spans, buf, keytype, starts, i_sta, i_doc):
  """
  Open tags. Takes `spans`, which is a tuple (x,y) where `x` tells
  us when a tag opens and `y` tells us when it closes.

  We add one openingn font tag per span.
  """
  if starts[i_sta][0] == i_doc:
    #print '\t\t\tSTARTS', i_doc, starts[i_sta][0]
    for span in spans:
      buf += '<font size=5px color="%s">' % KEYCOLOR[keytype[:-3]]
    #print '\t\t\tSTARTSi', i_sta
    return i_sta + 1, buf
  return i_sta, buf

def closeTags(spans, buf, ends, i_end, i_doc):
  """
  Closes open tags. Takes `spans`, which is a tuple (x,y) where `x` tells
  us when a tag opens and `y` tells us when it closes.

  We add one closing font tag per span.
  """
  if (ends[i_end][0]) == i_doc:
    #print '\t\t\tENDS', i_doc, ends[i_end][0]
    for span in spans:
      buf += '</font>'
    #print '\t\t\tENDSi', i_end
    return i_end + 1, buf
  return i_end, buf

def writeNonWord(buf, starts, ends, doc, keytype, i_sta, i_end, i_doc):
  """
  Writes non-word to the buffer. ONLY side effect is to alter buffer.
  """
  # close tags must close before we open new ones!
  i_end, buf = closeTags(ends[i_end][1], buf, ends, i_end, i_doc)
  # add char
  buf += doc[i_doc]
  # open tags
  i_sta, buf = openTags(starts[i_sta][1], buf, keytype, starts, i_sta, i_doc)
  i_doc += 1

  return i_sta, i_end, i_doc, buf

def writeWord(buf, starts, ends, word, keytype, i_sta, i_end, i_doc):
  """
  Writes non-word to the buffer. ONLY side effect is to alter buffer.
  """

  print 'BEFORE'
  print 'sta', i_sta, starts[i_sta]
  print 'end', i_end, ends[i_end]
  print 'doc', i_doc
  print len(word), i_doc + len(word)
  for i in range(len(word)):
    # close tags must close before we open new ones!
    i_end, buf = closeTags(ends[i_end][1], buf, ends, i_end, i_doc)
    # add char
    buf += word[i]
    # open tags
    i_sta, buf = openTags(starts[i_sta][1], buf, keytype, starts, i_sta, i_doc)
    i_doc += 1

  print 'AFTER'
  print 'sta', i_sta, starts[i_sta]
  print 'end', i_end, ends[i_end]
  print 'doc', i_doc

  print '\t', buf
  print

  if i_doc > 289:
    sys.exit()

  return i_sta, i_end, i_doc, buf

def docwordIdxToDocIdx(docwords, idx):
  return sum(map(lambda x: len(x), docwords[:idx]))



def annotateTrainingDoc(filename, document, docwords, kwindices, keytype):
  """
  Takes a the word_tokenized document, annotates according to the indices
  of the keywords, and then writes out.
  """
  for ind in kwindices:
    print docwords[ind[0]:ind[1]]

  doclower = document.lower()  # must be lower case to match our lem'd words
  i_doc = 0
  i_kwi = 0
  buf = ''
  print len(docwords), len(kwindices),
  print kwindices[i_kwi][0],
  print kwindices[i_kwi][1]
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





  # groups kwindices by starting index
  # this list looks like:
  #      [(i, [all spans beginning at index i...]), (j, [etc...])...]
  starts = [(it[0], [item for item in it[1]]) for it in
      groupby(kwindices, lambda x: x[0])]

  # groups kwindices by ending index
  kwindices_by_y_coord = sorted(kwindices, cmp=data.wordmapcmp_ycoord)
  ends = [(it[0], [item for item in it[1]]) for it in
      groupby(kwindices_by_y_coord, lambda x: x[1])]

  i_doc = 0  # walking through `document`
  i_sta = 0  # walking through `starts`
  i_end = 0  # walking through `ends`
  i_dwr = 0  # walking through `docwords`
  buf = ''  # holds progress on our completed document so far
  # walk over entire document; replace a word at a time with the marked
  # up version
  while True:
    if i_doc > len(document):
      break

    if i_dwr > len(docwords):
      if i_sta > len(starts) or i_end > len(ends):
        break

      # close tags must close before we open new ones!
      i_end, buf = closeTags(ends[i_end][1], buf, ends, i_end, i_doc)
      # add char
      buf += document[i_doc]
      # open tags
      i_sta, buf = openTags(starts[i_sta][1], buf, keytype, starts, i_sta, i_doc)

      i_doc += 1
      continue

    if i_sta > len(starts) or i_end > len(ends):
      print 'ERROR: i_sta or i_end reached the end of their list'
      sys.exit()

    #print 'idoc', i_doc, 'starts', i_sta, starts[i_sta][0], 'ends', i_end, ends[i_end][0], '\n', buf, '\n\n\n'
    #print docwords[i_dwr], document[i_doc]

    matched = re.match(docwords[i_dwr], document[i_doc:])
    # If we don't find the next docword, write char + tags to `buf`
    if not matched:
      i_sta, i_end, i_doc, buf = writeNonWord(buf, starts, ends, document, keytype,
          i_sta, i_end, i_doc)
      continue

    # Else, write word to `buf` and continue
    word = matched.group(0)

    i_sta, i_end, i_doc, buf = writeWord(buf, starts, ends, word, keytype, i_sta, i_end, i_doc)

    i_dwr += 1

  sys.exit()



  """
  identifier = data.filenameToIdent(filename)

  docwords = re.sub('\n\n', '<p><p>\n', docwords)
  docwords = re.sub('\n', '<br />\n', docwords)

  # Find keywords in docwords, annotate them
  """
  """
  kwords = key[3][identifier]
  for kword in kwords:
    print kword
  print key[3]
  """
  """
  kwords = key[3][identifier]
  for kword in kwords:
    for gram in kword.split():
      document = re.sub(gram, '<font size=5px color="%s"><b>%s</b></font>'
          % (KEYCOLOR[keytype[:-3]], gram), document)

    #print document
    return document,identifier + '_' + keytype
  """

def assemblePage(filepath, filename, document, keydict):
  """
  Assembles a single training document as marked-up HTML
  """

  page = ''  # Will contain out entire output page
  page += HEADER % (filename, filename)

  ident = data.filenameToIdent(filename)
  print ident
  # NOTE: THIS ALL ASSUMES YOU'RE USING STEMMED ANSWERS
  # TODO: THIS SHOULD NOT ASSUME YOU'RE USING STEMMED ANSWERS!
  words, stemmed = data.docWordMap(document)

  for t in data.KEY_TYPES:
    docansw = keydict[t][3][ident]
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


  sys.exit()

  # assemble doc
  page += FOOTER

  # Write out
  f = open(DIRECTORY + identifier + '.html', 'w')
  f.write(document)
  f.close()

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


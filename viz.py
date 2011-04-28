import re, sys

import data


# DIRECTORIES: where we store our marked-up HTML training stuff

DIRECTORY = 'trainingviz/'


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


def annotateTrainingDoc(filename, document, key, name):
  identifier = data.filenameToIdent(filename)

  document = re.sub('\n\n', '<p><p>\n', document)
  document = re.sub('\n', '<br />\n', document)

  # Find keywords in document, annotate them
  """
  kwords = key[3][identifier]
  for kword in kwords:
    print kword
  """
  print key[3]
  kwords = key[3][identifier]
  for kword in kwords:
    for gram in kword.split():
      document = re.sub(gram, '<font size=5px color="%s"><b>%s</b></font>'
          % (KEYCOLOR[name[:-3]], gram), document)

    #print document
    return document,identifier + '_' + name

def assemblePage(filepath, filename, document, keydict):
  """
  Assembles a single training document as marked-up HTML
  """

  page = ''  # Will contain out entire output page
  page += HEADER % (filename, filename)

  ident = data.filenameToIdent(filename)
  # NOTE: THIS ALL ASSUMES YOU'RE USING STEMMED ANSWERS
  # TODO: THIS SHOULD NOT ASSUME YOU'RE USING STEMMED ANSWERS!
  words, stemmed = data.docWordMap(document)

  for t in data.KEY_TYPES:
    docansw = keydict[t][3][ident]
    for answ in docansw:
      indices = [(i,j) for i,j in data.findAnswInWordMap(answ, stemmed)]
      indices.sort(cmp=data.wordmapcmp)
      """
      q = [(1,4), (2,3), (1,2), (3,4)]
      q.sort(cmp=data.wordmapcmp)
      print q
      for i in indices:
        print i
      """

      """
      # Do stuff here
      document,identifier = annotateTrainingDoc(filename, document, key, name)
      print identifier
      """


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


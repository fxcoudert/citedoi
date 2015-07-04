#!/usr/bin/env python

import sys, os, requests, json


def pmid2doi(pmid):
  """
  Return a DOI from a PubMed numeric identifier (PMID)
  """

  url = "http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + pmid + "&format=json&versions=no&tool=citedoi&email=me@me.com"
  r = requests.get(url)
  return json.loads(r.text)["records"][0]["doi"]

def doi2bib(doi):
  """
  Return a bibTeX string of metadata for a given DOI.
  """
 
  url = "http://dx.doi.org/" + doi
  headers = {"accept": "application/x-bibtex"}
  r = requests.get(url, headers = headers)
  return r.text

def replacebibkey(bib, key):
  y, z = bib.split(",", 1)
  x, y = y.split("{", 1)
  return x + "{" + key + "," + z

def iskeyalreadypresent(key, bibfile):
  try:
    f = open(bibfile, "r")
  except:
    return False

  for line in f:
    if line[0] == '@' and key in line:
      return True

  return False

def main():
  bibfile = sys.argv[1] + ".bib"
  doi = sys.argv[2]
  key = sys.argv[3]

  if iskeyalreadypresent(key, bibfile):
    return

  try:
    if doi[0:3] != "10.":
      # If not a DOI, resolve through PubMed
      doi = pmid2doi(doi)

    bib = doi2bib(doi)
  except:
    return

  bib = replacebibkey(bib, key)
  with open(bibfile, "a") as f:
    f.write(bib + "\n")

if __name__ == '__main__':
  main()

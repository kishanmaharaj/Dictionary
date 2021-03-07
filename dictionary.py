#!/usr/bin/env python

from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests
import sys
from tqdm import tqdm

def get_words(file_add):
    """
     Returns a list containg all the words from CSV file 
         Args:
             file_add (str): Address of CSV file with all the words
         Returns:
             list
    """

    word_csv = pd.read_csv(file_add)
    words = []
    for i in word_csv['word']:
        words.append(i)
    return words    


def get_meaning(word):

    """
     Returns a list containg all the meanings of word 
         Args:
             word (str): word for searching the meanings
         Returns:
             list
    """

    url = "https://googledictionary.freecollocation.com/meaning?word=" + word
    response = requests.get(url)
    soupBody = BeautifulSoup(response.content,features = "html.parser")
    text = soupBody.findAll("li", {"style" : "list-style:decimal"})
    meanings_with_codes = []
    for i in text: 
        meanings_with_codes.append(i.text)
    meanings_raw = []
    for i in range(0, len(meanings_with_codes)):
        if "-" in meanings_with_codes[i]:
            meanings_raw.append(meanings_with_codes[i][:meanings_with_codes[i].index("-")])
        else :
            meanings_raw.append(meanings_with_codes[i])
    meanings_1 = []
    for sub in meanings_raw:
        meanings_1.append(sub.replace("\n", ""))
    meanings = []
    for sub in meanings_1:
        meanings.append(sub.replace(";", " or"))     
    return meanings  




def meaning_extraction(words):
    """
     Returns a list rows containg all the meanings of all word in a 2D list format 
         Args:
             words (str): a list of all words for searching the meanings
         Returns:
             list

    """
    rows = []
    for i in tqdm(range(len(words)), desc = "Meaning Extraction"):
        meanings = get_meaning(words[i])
        x = []
        for j in (range(len(meanings))):
            x.append(meanings[j])
        rows.append([words[i]]+x)
    return rows    



def write_csv(filename,header,rows):
    """
     Returns None 
         Args:
             filename (str): name of the results file
             header (str): header of the results file
             rows (str): row wise data for results file containg words with meaning
         Returns:
             None
    """
    with open("results/"+filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(header)  
        csvwriter.writerows(rows)


def main(file_add,filename):
    """
     Returns None 
         Args:
             filename (str): name of the results file
             file_add (str): Address of CSV file with all the words
         Returns:
             None
    """
    words = get_words(file_add)
    rows = meaning_extraction(words)
    
    header = ["word","Meaning 1","Meaning 2", "Meaning 3", "Meaning 4"]
    write_csv(filename,header,rows)
    print("File Saved Successfully")

file_add = "data/" + sys.argv[1]
filename = sys.argv[2]

main(file_add,filename)


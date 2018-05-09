# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:37:25 2018

@author: Narendra_Mugada
"""

import re
import sys
from os import listdir

from flask import Flask
from flask import render_template
from flask import request
from flask.json import jsonify
app = Flask(__name__, static_url_path ="/images",static_folder = "images")
#search_str = "the"
dir_name = "C:/Users/narendra_mugada/PycharmProjects/Flask_Demo/text"
file_name = "C:/Users/narendra_mugada/PycharmProjects/Flask_Demo/text/apple.txt"

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/search')
def search():
    return render_template('SearchPage.html')

@app.route('/search',methods=['POST'])
def my_form():
    text=request.form['search']
    processed_text=text
    search_patterns=searchStringInDIR(processed_text,dir_name)
    #print(search_patterns)
    return search_patterns

if __name__ == '__main__':
   app.run(debug=True)

def searchStringInFile(str, file_name):
    file = open(file_name, "r", encoding="utf8")
    search_patterns = []
    user=""
    #print(str)
    for line in file:
        if re.search(str, line):
            search_patterns.append(line)
            user=user+line+"\n"
    #print(user)
    return search_patterns

def searchStringInDIR(str,directory):
    searchPatternsInDIR = list()
    # walk through all files in the folder
    for filename in listdir(directory):
        # create the full path of the file to open
        file_path = directory + '/' + filename
        searchPatternsInDIR.append({"File_Name": file_path,
                                    "File_Text": searchStringInFile(str, file_path)})
        print(searchStringInFile(str, file_path))
    return render_template('displayText.html', name=searchPatternsInDIR, lenparam=len(searchPatternsInDIR))
    #return print(searchStringInFile(str, file_path))
#searchPatternsInDIR = process_docs(dir_name)



#searchPatterns = searchStringInFile(str, file_name)

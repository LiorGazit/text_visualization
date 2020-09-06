# Text Visualization
This repo hosts various methods to visualize text insights, models, and relationships that drive value.

## ScatterText 
This is a fabulous visualization tool that lets you see which words characterize each class in the data set.    
It assumes you have a text data set, where each text observation belongs to **one of two** classes, and that there is a column dedicated to the class label (i.e., this is for a labeled data set, not for a set that is to be labeled).    
See [here for Jason Kesseler's development](https://github.com/JasonKessler/scattertext).    

### Set up:
Supper simple:   
`pip install scattertext`

### The Main Function that Does the "Magic"
The function `scattertext()`, which is inside the file:  
`JasonKessler_scattertext.py`  

### The Data Set
[Medical Information Extraction](https://appen.com/datasets/medical-sentence-summary-and-relation-extraction/),  
"*A dataset of relationships between medical terms in PubMed articles, for relation extraction and related natural language processing tasks.*"  
(Out of the 3 sets, I took the "train" set).  

You don't need to download it ahead of time, the code will download it for you if it doesn't fine the file in the local folder.  


#### Next
- Change the py file to be a NB that sources the basic scattertext() function (which would live in a py file)  
- Maybe transition to COLAB, as I believe I can get the HTML visual scattertext to work on COLAB (like I know how to deploy a streamlit webapp on COLAB)  
- Implement my own set of text preprocessing (stopwords, grouping, lemmatization, etc.) by probing the `corpus` variable after it's created  

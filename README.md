# Keyword Management Tool

The Keyword Manager is a tool to support SEAs and SEOs finding new keywords
from a website.
Just input the website you want to analyze and submit. You can also use options
to control the keyword output.
Create a user account to save and combine different keyword lists.
For futher use you can export the lists as csv document.

## Setup

You should have installed a current version (3+) of Python.

```
pip install django
pip install beautifulsoup4
pip install rake-nltk
```

## HowTo

Input the website you want to analyze and submit.

### Options

There are different options to control the keyword ouput:
- Website language: Choose the website's language. It's relevant for the used stopwords list.
- Number of keywords: Choose the amount of output keywords.
- Phrase length: Choose the phrase length. There is a minimum phrase length of one and a maximum of four.
- Terms to exclude: Input the terms that shouldn't appear in the output.

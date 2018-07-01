import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from rake_nltk import Rake

def get_html(url):
    """
    Function gets an url as parameter and returns the html as text (string)

    ToDo: Exception handling for not availble websites and other errors
    """
    page = requests.get(url)
    contents = page.content

    return contents

def tag_visible(element):
    """
    Helper function returns false, if element should be excluded, true otherwise.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_raw_text(html):
    """
    Function gets a html-string as parameter. All tags are removed from the
    html-string. In the end the function returns plain text.
    """
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text = True)
    visible_texts = filter(tag_visible, texts)

    return u" ".join(t.strip() for t in visible_texts)


def get_keywords(raw_text, language, phraseMinLength, phraseMaxLength):
    """
    Function gets the plain text as input and returns a list of keywords by
    using the RAKE-library.
    """
    r = Rake(min_length = int(phraseMinLength),
             max_length = int(phraseMaxLength),
             language=language)

    # Extraction given the text.
    r.extract_keywords_from_text(raw_text)

    # To get keyword phrases ranked highest to lowest with scores.
    return r.get_ranked_phrases_with_scores()

def get_filtered_keywords(keywords):
    """
    TODO: Filter keywords. Don't forget how list of keywords is build:
          [(12.0, "keyword1"), (10.2 "keyword2"), ...]
    """
    return keywords

def get_website_keywords(url, language, phraseMinLength, phraseMaxLength):
    """
    Functions gets different parameters and returns keywords consindering the
    commited options.
    """
    h = get_html(url)
    t = get_raw_text(h)
    k = get_keywords(t, language, phraseMinLength, phraseMaxLength)
    f = get_filtered_keywords(k)
    return k

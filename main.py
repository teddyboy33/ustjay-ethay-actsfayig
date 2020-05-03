"""
Tranlates a random fact into pig latin
Created by Philip Korte
"""

import os

import requests
from flask import Flask, send_file, Response, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """
    Retrieves a random fact from unkno.com
    """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def get_location(fact):
    """
    Retrieves the location of a piglatinized fact.
    """
    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    myobj = {'input_text': fact}

    response = requests.post(url, myobj, allow_redirects=False)

    my_location = response.headers['Location']
    return my_location


@app.route('/')
def home():
    """
    Returns a web page with a random fact and a link to it's translation.
    """
    fact = get_fact()
    url = get_location(fact)
    return render_template('translate.jinja2', fact=fact, url=url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

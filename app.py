from flask import Flask, jsonify
from flask import render_template
import json
import plotly.express as px
import pandas as pd
from publications import Publications
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from PIL import Image
import numpy as np
import os
import plotly

app = Flask(__name__)


@app.route('/publications', methods=['GET'])
def get_publications():
    # Create an instance of Publications
    pub = Publications()

    # Call the method to fetch publications and save them into a JSON file
    pub.fetch_publications()

    # Read the data from JSON file
    with open('data.json') as f:
        data = json.load(f)

    # Return the data as a list of dictionaries
    return jsonify(data), 200

def plot_histogram():
    # Assuming you have a pandas DataFrame named 'df' and 'Year' is the column with the publication year.
    df = pd.read_json('data.json')  
    df['Year'] = df['title'].apply(lambda x: x.split(', ')[-1])  # extract year from title

    fig = px.bar(df, x='Year')

    return fig.to_html(full_html=False)

hist = plot_histogram()

def plot_pie():
    data = pd.read_json('data.json')

    def split_authors(title):
        authors_section = title.split("\n")[1]
        authors = [author.strip() for author in authors_section.split(",")]
        return authors

    data['authors'] = data['title'].apply(split_authors)

    # Count the occurrences of each author
    author_counts = data['authors'].explode().value_counts()

    labels = author_counts.index
    values = author_counts

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                insidetextorientation='radial'
                                )])
    
    return fig.to_html(full_html=False)

def generate_wordcloud_plotly(datafile):
    # Load your json file into a pandas DataFrame
    df = pd.read_json(datafile)

    # Concatenate all the titles into one big string
    title_text = ' '.join(df['title'])

    # Generate a word cloud object and set parameters
    wordcloud = WordCloud(width=800, height=400, max_font_size=100, background_color="white").generate(title_text)

    # Display the word cloud and save it as a PNG
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud.png')
    plt.close()

    # Open the saved image with PIL (Python Imaging Library) and convert to array
    img = Image.open('wordcloud.png')
    img_array = np.array(img)

    # Delete the image file
    os.remove('wordcloud.png')

    # Create a figure in plotly
    fig = go.Figure(data=go.Image(z=img_array))

    # return the plotly figure
    return fig


@app.route('/')
def index():  # put application's code here
    publications = Publications()
    publications.fetch_publications()

    fig = generate_wordcloud_plotly('data.json')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    hist = plot_histogram()
    pie = plot_pie()

    return render_template(
        'index.html', plot1_html=hist, plot2_html = pie, fig_json=fig_json,
        title = 'Data Visualization Final'
    )


if __name__ == '__main__':
    app.run()

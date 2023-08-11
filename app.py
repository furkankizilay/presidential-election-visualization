import time
import os
from flask import Flask, render_template

from fetch import Fetcher
import unidecode
from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd  # pip install pandas
import numpy as np  # pip install numpy
import plotly.express as px  # pip install plotly
import plotly.graph_objects as go  # pip install plotly
# pip install plotly | subplot'lar yapmak için kullanacağız
from plotly.subplots import make_subplots
import requests  # pip install requests
import json

app = Flask(__name__)


def plot():
    df = pd.read_json('csv/SecimSonucIl.json')
    df.to_csv('file2.csv')

    # Load your data
    df = pd.read_csv('file2.csv')

    # Create a new DataFrame with only the rows where the ID is even
    df_even = df[df['Unnamed: 0'] % 2 == 0]

    # Save the new DataFrame to a new CSV file
    df_even.to_csv('newfile3.csv', index=False)

    df = pd.read_csv('newfile3.csv')
    df = df.drop("Unnamed: 0", axis=1)

    response = requests.get(
        'https://gist.githubusercontent.com/mebaysan/9be56dd1ca5659c0ff7ea5e2b5cf6479/raw/6d7a77d8a2892bd59f401eb87bd82d7f48642a58/turkey-geojson.json')
    # Gist üzerindeki raw dataya erişmek için adrese istek (get) atıyoruz

    geojson = response.json()

    df['Kayıtlı Seçmen Sayısı'] = df['Kayıtlı Seçmen Sayısı'].str.replace('.', '').astype('float64')
    df['Oy Kullanan Seçmen Sayısı'] = df['Oy Kullanan Seçmen Sayısı'].str.replace('.', '').astype('float64')
    df['Geçerli Oy Toplamı'] = df['Geçerli Oy Toplamı'].str.replace('.', '').astype('float64')
    df[' RECEP TAYYİP ERDOĞAN '] = df[' RECEP TAYYİP ERDOĞAN '].str.replace('.', '').astype('float64')
    df[' MUHARREM İNCE '] = df[' MUHARREM İNCE '].str.replace('.', '').astype('float64')

    geoDict = {}
    for i in geojson['features']:
        geoDict[i['properties']['name']] = i['id']
        
    df.loc[:, 'GeoID'] = 'Yok'

    # df içerisindeki bu 3 ilimizi geoDict içerisindeki isimleri ile değiştiriyoruz
    df.loc[df['İl Adı'] == 'Afyonkarahisar'] = df.loc[df['İl Adı']
                                                    == 'Afyonkarahisar'].replace('Afyonkarahisar', 'Afyon')
    df.loc[df['İl Adı'] == 'Elâzığ'] = df.loc[df['İl Adı']
                                            == 'Elâzığ'].replace('Elâzığ', 'Elazığ')
    df.loc[df['İl Adı'] == 'Hakkâri'] = df.loc[df['İl Adı']
                                            == 'Hakkâri'].replace('Hakkâri', 'Hakkari')

    df["İl Adı"] = geoDict.keys()

    df['GeoID'] = df['İl Adı'].apply(lambda x: geoDict[x])

    columns_to_consider = [' MUHARREM İNCE ', ' MERAL AKŞENER ', ' RECEP TAYYİP ERDOĞAN ',' SELAHATTİN DEMİRTAŞ ', ' TEMEL KARAMOLLAOĞLU ', ' DOĞU PERİNÇEK ']
    df['winner'] = df[columns_to_consider].idxmax(axis=1)

    fig = px.choropleth_mapbox(df,  # hangi veri seti
                            geojson=geojson,  # hangi geojson dosyası
                            locations='GeoID',  # geojson dosyasında id'e denk gelen, veri setindeki hangi değişken
                            color='winner',  # hangi Değişkene göre renk paleti
                            color_continuous_scale="dense",  # hangi renk paleti
                            # renklendirme için min ve max değerler aralığı
                            range_color=(df[' DOĞU PERİNÇEK '].min(),
                                            df[' RECEP TAYYİP ERDOĞAN '].max()),
                            # map başlangıç lat & lon
                            center={'lat': 38.7200, 'lon': 34.0000},
                            # labellar değişecek mi
                            #labels={'Tahmin-2019': '2019 Nüfus Tahmini'},
                            mapbox_style="carto-positron",  # mapbox stil
                            zoom=4.8,  # yakınlık
                            opacity=0.5,  # opacity
                            custom_data=[df[' RECEP TAYYİP ERDOĞAN '],
                                            df[' MUHARREM İNCE '], df[' MERAL AKŞENER ']]  # figure'e göndereceğimiz ekstra veriler
                            )
    fig.update_layout(title='Türkiye Cumhurbaşkanlığı Seçimi',)  # figure başlığı
                    #title_x=0.5  # Title'ın x eksenindeki pozisyonu
                    
    #  gönderdiğimiz customdata'nın ilk elemanı
    hovertemp = '<i style="color:red;">RECEP TAYYİP ERDOĞAN:</i> %{customdata[0]}<br>'
    hovertemp += '<i>MUHARREM İNCE:</i> %{customdata[2]}<br>'
    hovertemp += '<i>MERAL AKŞENER:</i> %{customdata[1]:,f}<br>'
    # figure üzerine gelince oluşturduğum stringi göster
    fig.update_traces(hovertemplate=hovertemp)
    return fig

def convert_json_to_csv(json_folder='csv/', csv_folder='ilce_csv/'):
    # JSON dosyalarını işlemek için döngü oluştur
    for file_name in os.listdir(json_folder):
        if file_name.startswith('SecimSonucIlce') and file_name.endswith('.json'):
            json_path = os.path.join(json_folder, file_name)

            # JSON dosyasını DataFrame'e yükle
            df = pd.read_json(json_path)

            # CSV olarak kaydet
            csv_file_name = file_name.split('.')[0] + '.csv'
            csv_path = os.path.join(csv_folder, csv_file_name)

            # Unnamed:0 sütunu varsa sil, yoksa aynı DataFrame'i kullan
            if 'Unnamed: 0' in df.columns:
                df.drop('Unnamed: 0', inplace=True, axis=1)

            # İlçe Id sütunu sayısal olmayan değerleri içeren satırları sil

            df = df[pd.to_numeric(df['İlçe Id'], errors='coerce').notnull()]

            df.to_csv(csv_path, index=False)

            # Gereksiz sütunları sil
            df.drop("Mahaller Bazlı Veri İndir", inplace=True, axis=1)
            df = df[pd.to_numeric(df['İlçe Id'], errors='coerce').notnull()]

            # Indexleri düzelt
            df.reset_index(drop=True, inplace=True)

            # Tek sayı indexlere sahip satırları sil
            df.drop(df[df.index % 2 == 1].index, inplace=True)
            df.reset_index(drop=True, inplace=True)

            # İşlenmiş DataFrame'i kullanarak istediğiniz işlemleri gerçekleştirin
            # ...

            # Sonuçları kontrol etmek için örnek bir yazdırma
            print(f"{file_name} işlendi. Toplam satır sayısı: {len(df)}")

def plot_histogram():
    # Load the JSON data
    with open('csv/SecimSonucIl.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove the second objects from each province
    province_data = [d for i, d in enumerate(data) if i % 2 == 0]

    # Initialize an empty dictionary to store total votes for each candidate
    votes = {' MUHARREM İNCE ': 0, ' MERAL AKŞENER ': 0, ' RECEP TAYYİP ERDOĞAN ': 0, ' SELAHATTİN DEMİRTAŞ ': 0, ' TEMEL KARAMOLLAOĞLU ': 0, ' DOĞU PERİNÇEK ': 0}

    # Sum up the votes from each province
    for province in province_data:
        for candidate in votes.keys():
            # Use stripped keys in the province dictionary
            votes[candidate] += int(province[candidate].replace(".", "").strip())

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(votes.items()), columns=['Candidate', 'Votes'])

    # Sort by votes
    df = df.sort_values('Votes', ascending=False)

    # Draw the histogram using plotly
    fig = px.bar(df, x='Candidate', y='Votes', title='Total Votes for Each Presidential Candidate')
    
    return fig.to_html(full_html=False)



def istanbul_plot():

    # Load the JSON data
    with open('csv/SecimSonucIlce (39).json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove the first and third objects from each district
    district_data = [d for i, d in enumerate(data) if i % 3 == 1]

    # Initialize an empty dictionary to store total votes for each candidate
    votes = {' MUHARREM İNCE ': 0, ' MERAL AKŞENER ': 0, ' RECEP TAYYİP ERDOĞAN ': 0, ' SELAHATTİN DEMİRTAŞ ': 0, ' TEMEL KARAMOLLAOĞLU ': 0, ' DOĞU PERİNÇEK ': 0}

    # Sum up the votes from each district
    for district in district_data:
        for candidate in votes.keys():
            # Use stripped keys in the district dictionary
            votes[candidate] += int(district[candidate].replace(".", "").strip())

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(votes.items()), columns=['Candidate', 'Votes'])

    # Sort by votes
    df = df.sort_values('Votes', ascending=False)

    labels = df["Candidate"]

    values = df["Votes"]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                insidetextorientation='radial'
                                )])
    
    return fig.to_html(full_html=False)

def izmir_plot():

    # Load the JSON data
    with open('csv/SecimSonucIlce (40).json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove the first and third objects from each district
    district_data = [d for i, d in enumerate(data) if i % 3 == 1]

    # Initialize an empty dictionary to store total votes for each candidate
    votes = {' MUHARREM İNCE ': 0, ' MERAL AKŞENER ': 0, ' RECEP TAYYİP ERDOĞAN ': 0, ' SELAHATTİN DEMİRTAŞ ': 0, ' TEMEL KARAMOLLAOĞLU ': 0, ' DOĞU PERİNÇEK ': 0}

    # Sum up the votes from each district
    for district in district_data:
        for candidate in votes.keys():
            # Use stripped keys in the district dictionary
            votes[candidate] += int(district[candidate].replace(".", "").strip())

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(votes.items()), columns=['Candidate', 'Votes'])

    # Sort by votes
    df = df.sort_values('Votes', ascending=False)

    labels = df["Candidate"]

    values = df["Votes"]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                insidetextorientation='radial'
                                )])
    
    return fig.to_html(full_html=False)

def ankara_plot():

    # Load the JSON data
    with open('csv/SecimSonucIlce (6).json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove the first and third objects from each district
    district_data = [d for i, d in enumerate(data) if i % 3 == 1]

    # Initialize an empty dictionary to store total votes for each candidate
    votes = {' MUHARREM İNCE ': 0, ' MERAL AKŞENER ': 0, ' RECEP TAYYİP ERDOĞAN ': 0, ' SELAHATTİN DEMİRTAŞ ': 0, ' TEMEL KARAMOLLAOĞLU ': 0, ' DOĞU PERİNÇEK ': 0}

    # Sum up the votes from each district
    for district in district_data:
        for candidate in votes.keys():
            # Use stripped keys in the district dictionary
            votes[candidate] += int(district[candidate].replace(".", "").strip())

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(votes.items()), columns=['Candidate', 'Votes'])

    # Sort by votes
    df = df.sort_values('Votes', ascending=False)

    labels = df["Candidate"]

    values = df["Votes"]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                insidetextorientation='radial'
                                )])
    
    return fig.to_html(full_html=False)


figure = plot()
# convert_json_to_csv()


@app.route('/')
def index():  # put application's code here

    """fetcher = Fetcher()
    fetcher.driver.get('https://acikveri.ysk.gov.tr/anasayfa')
    fetcher.driver.maximize_window()
    fetcher.navigate_to_button('myModalClose')
    fetcher.navigate_to_button('navbarDropdown')
    time.sleep(1)
    fetcher.navigate_to_button('heading6')
    time.sleep(1)
    fetcher.navigate_to_button('collapse6')
    time.sleep(1)
    fetcher.navigate_to_link('Cumhurbaşkanlığı Seçim Sonuçları')
    time.sleep(2)
    fetcher.navigate_to_button_xpath('//*[@id="kadinErkekOraniBar"]/div[2]/div/button[2]')
    time.sleep(5)


    fetcher.click_buttons_by_city()
    time.sleep(2)
    fetcher.close()"""


    # Plotly figürünü oluştur. (Örneğin bir scatter plot)
    fig = go.Figure(
            figure,
    )

    sum_of_votes = plot_histogram()
    istanbul_figure = istanbul_plot()
    izmir_figure = izmir_plot()
    ankara_figure = ankara_plot()


    # Plotly figürünü HTML string olarak dönüştür.
    # Çıktıdaki <div> elementinin ID'si otomatik olarak oluşturulur.
    div = pio.to_html(fig, full_html=False)

    # index.html dosyasını HTML string ile birlikte renderla.
    return render_template("index.html", plot_div=div, plot0_html = sum_of_votes, plot1_html=istanbul_figure, plot2_html=ankara_figure,plot3_html=izmir_figure)


    """return render_template(
        'index.html',
        title='Election Results'

    )"""


if __name__ == '__main__':
    app.run()

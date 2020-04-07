from flask import Flask
from flask import render_template
#from flask import request
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#imports for map creation
import folium
#from folium import plugins
#import geocoder
#import geopy
#import numpy as np
import pandas as pd
#from folium.plugins import FastMarkerCluster
from folium.features import DivIcon
import os.path

my_path = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():


    url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/covid-19-cases-by-notification-date-and-postcode-local-health-district-and-local-government-area.csv'
    #url1 = 'https://www.corra.com.au/downloads/Australian_Post_Codes_Lat_Lon.zip'
    path = os.path.join(my_path, "Australian_Post_Codes_Lat_Lon.csv")
    df = pd.read_csv(path)
    df1 = pd.read_csv(url)


    #remove any rows that have any value as a nan
    df1 = df1.dropna()


    #make a list of all postcodes that have covid cases and remove duplicate postcodes
    pc_list = df1['postcode'].tolist()
    pc_list = list(set(pc_list))

    #create a dict Key = suburb, value = number of covid cases
    count_persub = df1['postcode'].value_counts().to_dict()

    #reduce lat and lon df to only those postcodes with covid cases and again remove duplictes
    df = df[df['postcode'].isin(pc_list)]
    df = df.drop_duplicates(subset = ['postcode'])



    #create a map with start loc at Mosman
    folium_map = folium.Map([-33.829077, 151.244090], zoom_start=12)


    #iterate through lat and lon df of suburbs with covid cases, add a marker with the number of cases for each suburb
    for index, row in df.iterrows():
        text = count_persub[row["postcode"]]
        folium.map.Marker([row["lat"], row["lon"]],
                            icon=DivIcon(
                            icon_size=(70,18),
                            icon_anchor=(0,0),
                            html=f'<div style="font-size: 16pt">{text}</div>')
                            ).add_to(folium_map)

    #save map to current dir
    path = os.path.join(my_path, "templates/cvmap.html")
    folium_map.save(path)







    return render_template('cvmap.html')

# @app.route('/upload_pic', methods=['POST'])
# def upload_pic():
#     photo_object = request.files['pic']
#     target = os.path.join(APP_ROOT, 'images/')
#     filename = photo_object.filename
#     destination = '/'.join([target, filename])
#
#     photo_object.save(destination)
#
#
#
#     return render_template('pic_saved.html')
#


if __name__ == '__main__':
    app.run()

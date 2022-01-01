from flask import Flask
from flask import render_template
from flask import request
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#imports for map creation
import folium
from folium import plugins
import pandas as pd
from folium.features import DivIcon
import numpy as np
from datetime import datetime, timedelta



app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():


    #url1 = 'https://www.corra.com.au/downloads/Australian_Post_Codes_Lat_Lon.zip'
    url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv'

    target1 = os.path.join(APP_ROOT, 'Australian_Post_Codes_Lat_Lon.csv')
    df = pd.read_csv(target1)
    #target2 = os.path.join(APP_ROOT, 'confirmed_cases_table1_location.csv')
    df1 = pd.read_csv(url)

    #remove any rows that have any value as a nan
    df1 = df1.replace(to_replace='None', value=np.nan).dropna()

    #Generate current date in format to match df1
    # date = datetime.today().strftime('%Y-%m-%d')
    tod = datetime.today()
    fortnightAgo = (tod - timedelta(days=14)).strftime('%Y-%m-%d')
    #print(fortnightAgo)

    #Remove entries for covid cases older than 2 weeks
    df1 = df1[df1['notification_date'] >= fortnightAgo]
    #print(df1)

    #make a list of all postcodes that have covid cases and remove duplicate postcodes
    pc_list = df1['postcode'].tolist()
    pc_list = list(set(pc_list))
    pc_list = [int(i) for i in pc_list]


    #create a dict Key = suburb, value = number of covid cases
    count_persub = df1['postcode'].value_counts().to_dict()
    count_persub = {int(k):v for k,v in count_persub.items()}
    #print(count_persub)


    #reduce lat and lon df to only those postcodes with covid cases and again remove duplictes
    df = df[df['postcode'].isin(pc_list)]
    df = df.drop_duplicates(subset = ['postcode'])




    #create a map with start loc at Mosman
    folium_map = folium.Map([-33.829077, 151.244090], zoom_start=12)


    #iterate through lat and lon df of suburbs with covid cases, add a marker with the number of cases for each suburb
    for index, row in df.iterrows():
        text = count_persub[row['postcode']]
        folium.map.Marker([row['lat'], row['lon']],
                            icon=DivIcon(
                            icon_size=(70,18),
                            icon_anchor=(0,0),
                            html=f'<div style="font-size: 16pt">{text}</div>')
                            ).add_to(folium_map)


    #save map to current dir
    targ = os.path.join(APP_ROOT, 'templates/cvmap.html')
    folium_map.save(targ)







    return render_template('cvmap.html')



# if __name__ == '__main__':
#     app.run()
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

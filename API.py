#import library
import flask
import re
import sqlite3
import pandas as pd
import base64
import os

##import packages flask
from flask import Flask,request,jsonify,send_file,redirect

## import packages swagger
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

#Import Function
from Function import clean_text
from Function import cleansing_tweet
from Function import normalize_alay


### MENDEFENISIKAN FLASK ###
app = Flask(__name__)

# Rute untuk mengarahkan langsung ke dokumentasi Swagger UI
@app.route('/')
def index():
    return redirect('/docs')

def open_browser():
    import webbrowser
    webbrowser.open('http://localhost:5000/docs')

###  MENDEFENISIKAN SWAGGER ###
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Cleansing Data'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk proses pembersihan dan pemodelan data'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)


########## BODY API : ISIAN API ##########

###App(input_teks)###
@swag_from("docs_challenge/text_processing.yml", methods=['POST'])
@app.route('/input_teks', methods=['POST'])
def input_teks():
    data = request.form.get('text')
    data_umur = request.form.get('umur')
    data_uper = clean_text(data)

    json_response = {
        'output': data_uper, 
        'umur': data_umur
    }
    return jsonify(json_response)

### App(Upload_file) ###
@swag_from("docs_challenge/text_processing_file.yml", methods=['POST'])
@app.route('/input_file', methods=['POST'])
def data_processing():
    data_input = request.files['file']
    contents = data_input.read()
    output_directory = 'eglin-dsc/Challenge/Result_Data'
    output_file_path = os.path.join(output_directory, 'file.csv')
    
    # Check Directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    #convert dari encode ke decode
    encoded_contents = base64.b64encode(contents).decode('utf-8')
    decoded_contents = base64.b64decode(encoded_contents.encode(encoding='iso-8859-1'))
    
    #save the decode content to file 
    with open(output_file_path, 'wb') as f:
        f.write(decoded_contents)
        
# I. Membuat data base dan menggungah file.csv kedalam database
    conn = sqlite3.connect('data_tweet.db')
    path = 'eglin-dsc/Challenge/Result_Data/file.csv'
    df = pd.read_csv(path, encoding='iso-8859-1')
    df.to_sql('df', conn, if_exists='append', index = False)
    
# II. Cleansing data
    
    # 1. Memebersihkan Data dengan Regex
    # deskripsi : menghapus kata-kata yang tidak dibuthkan di dalam tweet, keterangan ada di file function.py
    pd.read_sql_query("""
                    SELECT 
                        Tweet
                    FROM df
                  """, conn)
    
    df['new_Tweet'] = df['Tweet'].apply(cleansing_tweet)
    
    # 2. Mengubah huruf kapital menjadi huruf kecil
    df['new_Tweet'] = df['new_Tweet'].apply(lambda x: x.lower() if isinstance(x, str) else x)
    
    # 3. membersihkan kata-kata alay dengan new_kamus_alay
    df['new_Tweet'] = df['new_Tweet'].apply(normalize_alay)
    
    # 4. Menambahkan kolom new_Tweet ke dalam tabel df
    df.to_sql('df', conn, if_exists='replace', index = False) # Jika sudah ada tabel df, gunakan if_exists='replace' untuk menggantinya
    
    
# III Convert the cleansed data to CSV format 
    cleansed_file_path = os.path.join(output_directory, 'cleansed_file.csv')
    df.to_csv(cleansed_file_path, index=False)
    
# IV Menampilkan hasil cleansing data ke API

    cleansed_tweets = df['new_Tweet'].tolist()
    #Respon Json  
    json_response = {
        'output': cleansed_tweets,
    }
    return jsonify(json_response)

## running API
if __name__ == '__main__':
   app.run()



    

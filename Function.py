import re
import flask
import base64
import os
import pandas as pd


##import request flask
from flask import request
from flask import jsonify
from flask import Flask, jsonify

def cleansing_tweet (tweet):
    tweet = re.sub('USER','',tweet)             #menghapus kata user
    tweet = re.sub('RT','',tweet)               #menghapus kata RT(re-tweet)
    tweet = re.sub(r'[^a-zA-Z0-9]',' ',tweet)   #mengganti kata non alphanumeric dengan spasi
    tweet = re.sub(r'https\S+', '',tweet)       #menghapus kata URL
    tweet = re.sub(r'[^\x08-\x7f]',r'',tweet)   #menghapus kata unique code
    tweet = re.sub('\?','',tweet)               #menghapus tanda tanya
    tweet = re.sub('/na','',tweet)              #menghapus kata /na
    tweet = re.sub(r'www\.[^ ]+', '',tweet)     #menghapus URL
    tweet = re.sub(r'x[a-f0-9]{2}', '',tweet)   #menghapus unique code x0F,xaa dan sebagainya
    tweet = re.sub(r'^\s+', '', tweet)          #menghapus tab sebelum kalimat 
    tweet = re.sub(r'\s+', ' ', tweet)          #menghapus double spasi
    return tweet

def clean_text (text):
    text = re.sub('http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    text = text.lower()

    return text

def normalize_alay(tweet):
    path_kamus_alay = 'eglin-dsc/Challenge/Dictionary_Challenges/new_kamusalay.csv'
    df_kamus_alay = pd.read_csv(path_kamus_alay, encoding='iso-8859-1')
    
    alay_dict_map = dict(zip(df_kamus_alay['Before'],df_kamus_alay['After']))
    alay_dict_map
    return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in tweet.split(' ')])


#belum diimplementasikan

# def input_teks():
#     data = request.form.get('text')
#     data_umur = request.form.get('umur')
#     data_uper = clean_text(data)

#     json_response = {
#         'output': data_uper, 
#         'umur': data_umur
#     }
#     return jsonify(json_response)



# def data_processing():
#     data_input = request.files['file']
#     contents = data_input.read()
#     output_directory = 'eglin-dsc/Challenge/Result_Data'
#     output_file_path = os.path.join(output_directory, 'file.csv')
    
#      # Ensure the output directory exists
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)
    
#     #convert dari encode ke decode
#     encoded_contents = base64.b64encode(contents).decode('utf-8')
#     decoded_contents = base64.b64decode(encoded_contents.encode(encoding='iso-8859-1'))
    
#     #save the decode content to file 
#     with open(output_file_path, 'wb') as f:
#         f.write(decoded_contents)
        
#     json_response = {
#         'output': decoded_contents.decode(encoding='iso-8859-1'),
#         'file_path': output_file_path
#     }
#     return jsonify(json_response)
##import flask
from flask import Flask, jsonify
import re
import gradio as gr
import pandas as pd

##import request
from flask import request


## import packages swagger
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


### mendefenisikan flask
app = Flask(__name__)

def clean_text (text):
    text = re.sub('http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    text = text.lower()

    return text

##defenisikan swagger

app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Try API Chapter 3'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API'),
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


##Body api : isi APInya

@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'data': "Hello World"
    }
    return jsonify(json_response)

@swag_from("docs_challenge/hello_world.yml",methods=['GET'])
@app.route('/',methods=['GET'])
def helloworld():
    data = request.get_data('teks')
    
    json_response = {
        "Output": data
    } 
    return jsonify(json_response)

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

@swag_from("docs_challenge/text_processing_file.yml", methods=['POST'])
@app.route('/input_teks', methods=['POST'])
def data_processing(file_obj):


    # Import file csv ke Pandas
    df = pd.read_csv(file_obj.name)
    

gradio_ui = gr.Interface(data_processing, 
                            title="Data Processing and Modeling",
                            description="Aplikasi Web Data Processing dan Modeling",
                            inputs="file", 
                            outputs="json")

gradio_ui.launch()


## running API
if __name__ == '__main__':
    app.run()

    

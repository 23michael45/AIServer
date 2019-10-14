import numpy as np
from PIL import Image as PILImage
from ImageClassifier.AIModule import getShape
from io import BytesIO

import json
from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os



def WriteJson(dict):
    jstr = json.dumps(dict)
    print(jstr)
    return jstr

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

mac_ip_dict = {}

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


@app.route('/Image', methods=['POST'])
def Image():
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info('FileName: ' + filename)
            
            data = file.stream.read();
            
            byte_stream = BytesIO(data);
            image = PILImage.open(byte_stream)

            jdict = {"category":"shape", "color":"0","shape":"xxx"}
            jdict['shape'] = getShape(np.asarray(image))

            return WriteJson(jdict)

@app.route('/MACandLIP', methods=['POST'])
def MACandLIP():
    if request.method == 'POST':
        encode_json = request.get_data()
        decode_json = json.loads(encode_json)
        mac_ip_dict[decode_json['MAC']] =decode_json['LIP']

        jdict = {'status': 'ok'}
        return WriteJson(jdict)

@app.route('/MAC', methods=['POST'])
def MAC():
    if request.method == 'POST':
        encode_json = request.get_data()
        decode_json = json.loads(encode_json)
          
        mac = decode_json['MAC']
            
        jdict = {'MAC': '','LIP':''}
        jdict['MAC'] = mac;

        if mac in mac_ip_dict:
            jdict['LIP'] = mac_ip_dict[mac];

        return WriteJson(jdict)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)

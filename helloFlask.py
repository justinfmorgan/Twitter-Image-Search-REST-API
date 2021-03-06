from flask import Flask, escape, request, redirect, send_file, render_template
from flask_restful import Resource, Api
import zipfile
from multiProcessing import *
import os

app = Flask(__name__)
api = Api(app)

data = 0

HOST = '0.0.0.0'
PORT = 8080

@app.route('/', methods=['GET', 'POST'], host=HOST)
def mainPage():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'], host=HOST)
def download_all():
    data = request.form['searchTerms']
    searchList = (str(data)).split(',')
    print(searchList)
    processVideos(searchList)
    zipf = zipfile.ZipFile('videos.zip','w', zipfile.ZIP_DEFLATED)
    for root,dirs,files in os.walk('searchVideos/'):
        for file in files:
            zipf.write('searchVideos/'+str(file))
    zipf.close()
    return send_file('videos.zip',
            mimetype = 'zip',
            attachment_filename= 'videos.zip',
            as_attachment = True)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
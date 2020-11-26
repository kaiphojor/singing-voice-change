from flask import Flask, render_template
from flask import url_for, redirect
from flask import g
from flask import request
import time
# flask 초기화, 이름을 포함함
app = Flask(__name__)
# error 보기위한 용도, debug 용도
app.debug = True


@app.route('/',host='index.html')
def index():
  return render_template('index.html')

@app.route('/tts',methods = ['POST','GET'])
def tts():
    if request.method == 'POST':
        text = request.form['tts-text']
        return render_template('text-to-speech.html',singer=text)
    elif request.method == 'GET':
        singer = request.args.get('singer','iu')
        return render_template('text-to-speech.html',singer=singer)
@app.route('/create',methods = ['POST'])
def gettext(display=None):
    if request.method == 'POST':
        text = request.form['tts-text']
        # query
        time.sleep(2)

        return render_template("done.html", display=text)

# @app.route('/tts', methods=['POST'])
# def my_form_post():
#     # text = request.form['text']
#     text = request.form.get('text',1)
#     # processed_text = text.upper()
#     return text

@app.route('/generic')
def generic():
    # request.form['']
  return render_template('generic.html')
@app.route('/elements.html')
def elements():
  return render_template('elements.html')
if __name__ == '__main__':
    app.run()

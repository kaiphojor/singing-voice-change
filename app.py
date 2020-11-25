from flask import Flask, render_template
from flask import url_for, redirect
from flask import g
from flask import request

# flask 초기화, 이름을 포함함
app = Flask(__name__)
# error 보기위한 용도, debug 용도
app.debug = True


@app.route('/',host='index.html')
def index():
  return render_template('index.html')

@app.route('/tts')
def tts():
  return render_template('text-to-speech.html')

@app.route('/generic')
def generic():
    # request.form['']
  return render_template('generic.html')
@app.route('/elements.html')
def elements():
  return render_template('elements.html')
if __name__ == '__main__':
    app.run()

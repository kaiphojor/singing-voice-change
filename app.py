from flask import Flask, render_template, request, send_file , Response
from flask import url_for, redirect
from flask import g
from flask import session
import time
# file download 용
from flask import send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
# flask 초기화, 이름을 포함함
app = Flask(__name__)
# error 보기위한 용도, debug 용도

app.debug = True
import os

# 메인 화면
@app.route('/',host='index.html')
def index():
  return render_template('index.html')

# TODO: 화면 미완성
# singing voice conversion 메뉴
@app.route('/svc',methods = ['GET'])
def svc():
    if request.method == 'GET':
        singer = request.args.get('singer', 'iu')
        # 음악 제목
        title = request.args.get('title', 'iu')
        return render_template('svc.html', singer=singer,title=title)

# TODO: 화면 미완성
# singing voice conversion 결과창
@app.route('/svc_result')
def svc_result():
    if request.method == 'GET':
        singer = request.args.get('singer', 'iu')
        return render_template('svc_result.html', singer=singer)

# text to speech 메뉴
@app.route('/tts',methods = ['GET'])
def tts():
    if request.method == 'GET':
        singer = request.args.get('singer','iu')
        return render_template('tts.html',singer=singer)
# text to speech 결과 화면
@app.route('/tts_result',methods = ['POST'])
def tts_result(display=None):
    if request.method == 'POST':
        #tts 텍스트가 넘어간 부분
        text = request.form['tts-text']
        # singer 정보 전달
        singer = request.form['singer']
        # 현재 날짜로 저장
        # TODO - 다른 사용자가 동시에 접근한다면? 나중에 처리
        datestring = str(datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f'))
        file_name = datestring+'.txt'
        # 파일 저장
        with open('tts_storage/text/'+datestring+'.txt','w',encoding='utf-8') as file :
            # 개행문자 제거, 공백 처리 , 마침표 기준 분할, 공백 줄 제거, 공백제거
            newline_removed_string = text.replace('\n',"").strip()
            period_separated_lines = [line.strip() for line in newline_removed_string.split('.') if line ]
            # print(period_separated_lines)
            # 마침표 및 개행 추가하여 저장
            for line in period_separated_lines :
                file.write(line + '.\n')
        # 로딩부분을 보여주기 위한 sleep
        # print(text)
        # query
        # time.sleep(2)
        # text 와 가수 정보, 생성한 파일 정보를 넘긴다.
        return render_template("tts_result.html", display=text,singer=singer,file_name=file_name)

# speech to speech 메뉴
@app.route('/sts',methods = ['GET'])
def sts():
    if request.method == 'GET':
        singer = request.args.get('singer','iu')
        return render_template('sts.html', singer=singer)
# speech to speech 결과 화면
@app.route("/sts_result",methods=['POST'])
def sts_result():
    #Moving forward code
    # stt 코드 실행
    forward_message = "Moving Forward..."
    # singer 정보 전달
    singer = request.form['singer']
    # print(forward_message)
    # 결과 페이지로 redirect 해야함
    return render_template("sts_result.html", message=forward_message,singer=singer);

# tts file download
@app.route('/download_tts',methods=['GET','POST'])
def download_tts():
    if request.method == 'POST' :
        # files = os.listdir('./tts_storage')
        path = './tts_storage/text/'
        # POST로 전달받은 파일이름을 이용하여 다운로드
        file_name = request.form['file_name']
            # 'test.txt'
        return send_file(path + file_name,
                         attachment_filename=file_name,
                         as_attachment=True)


# @app.route('/svc_storage/<path:filename>')
# def download_file(filename):
#     return send_from_directory('/svc_storage/', filename)

# # singing voice conversion 음악실행을 위한 routing
# @app.route('/svc_storage/<path:filename>')
# def play_svc_wav(filename):
#     print(filename)
#     return send_from_directory('/svc_storage/',filename)

# @app.route("/wav/<path:filename>")
# def streamwav(filename):
#     def generate():
#         with open("static/na.wav", "rb") as fwav:
#             data = fwav.read(1024)
#             while data:
#                 yield data
#                 data = fwav.read(1024)
#     return Response(generate(), mimetype="audio/x-wav")
#

# 쓰지 않으나 참고하는 부분

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # 경로 + 파일 명 - 미완성
        file.save('c:/'+secure_filename(file.filename))
        return 'file upload 성공!'
@app.route('/generic')
def generic():
  return render_template('generic.html')
# audio 저장
@app.route('/test')
def test():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        return render_template('upload_test.html', request="POST")
    else:
        return render_template('upload_test.html')

@app.route('/elements.html')
def elements():
  return render_template('elements.html')

if __name__ == '__main__':
    app.run()

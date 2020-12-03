from flask import Flask, render_template, request, send_file , Response, jsonify
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

# singing voice conversion 음악 선택 메뉴
@app.route('/svc_select_music',methods = ['GET'])
def svc_select_music():
    if request.method == 'GET':
        # 가수 이름 - 앨범커버 교체 위한 변수
        singer = request.args.get('singer', 'iu')
        print('가수 : ' + singer)
        files = list()
        files.append(dict(title='파일 이름', singer_list=['iu','lee-moon-se']))
        files.append(dict(title='파일 이름2',singer_list=['iu','lee-moon-se']))
        # files = ['asdf','fdzas','sdfew']
        print(files)
        for file in files :
            print(file['title'])
            print(file['singer_list'])
        return render_template('svc_select_music.html', singer=singer,files=files)

# singing voice conversion 아티스트 선택 메뉴
@app.route('/svc_select_artist',methods = ['GET'])
def svc_select_artist():
    if request.method == 'GET':
        # 가수 이름 - 앨범커버 교체 위한 변수
        singer = request.args.get('singer', 'iu')
        title = request.args.get('title','default')
        print('가수 : ' + singer)
        print('노래제목 : ' + title)
        return render_template('svc_select_artist.html', singer=singer,title=title)


# singing voice conversion 메뉴
@app.route('/svc',methods = ['GET'])
def svc():
    if request.method == 'GET':
        # 가수 이름 - 앨범커버 교체 위한 변수
        singer = request.args.get('singer', 'iu')
        # title - 재생할 파일 불러오기, 제목 설정에 쓰임
        title = request.args.get('title', 'iu')
        return render_template('svc.html', singer=singer,title=title)

# text to speech 메뉴
@app.route('/tts',methods = ['GET'])
def tts():
    if request.method == 'GET':
        singer = request.args.get('singer','iu')
        return render_template('tts.html',singer=singer)
# TODO: 결과파일이 나올때 저장 위치에 따라 수정(S3 / ec2)
# text to speech 결과 화면
@app.route('/tts_result',methods = ['POST'])
def tts_result(display=None):
    if request.method == 'POST':
        #tts 텍스트가 넘어간 부분
        text = request.form['tts-text']
        # singer 정보 전달
        singer = request.form['singer']
        # 현재 날짜로 저장
        # TODO - 다른 사용자가 동시에 접근한다면? 추후 처리
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
        # TODO: tts 돌리고 나서 결과물의 파일 이름만 file_name에 보내면 될 듯하다
        # 생성한 파일은 S3에 저장되면 링크만을 가져오면 된다. 아닌 경우에는 static에만 저장해서 불러와야 한다.
        # TODO: 임시저장은 나중에 구현
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
# TODO: 결과파일이 나올때 저장 위치에 따라 수정(S3 / ec2)
# speech to speech 결과 화면
@app.route("/sts_result")
def sts_result():
    #Moving forward code
    # stt 코드 실행
    forward_message = "Moving Forward..."
    # singer 정보 전달
    singer = request.values.get('singer')

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
        return send_file(path + file_name,
                         attachment_filename=file_name,
                         as_attachment=True)

# 녹음 버튼 눌렀을 때
# 버튼을 한번누르면 넘어가는 state값이 ready -> recording으로 바뀐다
@app.route('/record',methods=['POST'])
def record():
    if request.method == 'POST' :
        data = request.get_json()
        flag = data['state']
        singer = data['singer']
        if(flag == 'ready') :
            # 처음 녹음 버튼 눌렀을 때 동작

            return jsonify(result="success", result2=data)
        else :
            # 다시 녹음버튼을 눌렀을 때 동작

            return jsonify(result="success", result2=data)


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

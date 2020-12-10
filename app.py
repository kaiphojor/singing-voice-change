from flask import Flask, render_template, request, send_file , Response, jsonify
from flask import url_for, redirect
from flask import g
from flask import session
import time
from flask import send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
import speech as voiceConv
import voice_conversion.sts as s2s
import text_to_speech as textConv
import text_conversion.tts as t2s
import shutil

app = Flask(__name__)


app.debug = True


# 메인 화면
@app.route('/',host='index.html')
def index():
  return render_template('index.html')
# menu 화면들
@app.route('/svc_menu')
def svc_menu():
    return render_template('svc_menu.html')
@app.route('/tts_menu')
def tts_menu():
    return render_template('tts_menu.html')
@app.route('/sts_menu')
def sts_menu():
    return render_template('sts_menu.html')

# singing voice conversion 아티스트 선택 메뉴
@app.route('/svc_select_artist',methods = ['GET'])
def svc_select_artist():
    if request.method == 'GET':
        # 가수 이름 - 앨범커버 교체 위한 변수
        singer = request.args.get('singer', 'iu')
        # title = request.args.get('title','default')
        print('선택된 원곡 가수 : ' + singer)
        # print('노래제목 : ' + title)

        # 여기서 title 별 바꾸고자 하는 가수를 설정 해줌
        target_singers = list()
        if(singer == 'jang'):
            target_singers.append('iu')
        else :
            target_singers.append('jang')
        # title = title,
        return render_template('svc_select_artist.html', singer=singer,target_singers=target_singers)

# singing voice conversion 음악 선택 메뉴
@app.route('/svc_select_music',methods = ['GET'])
def svc_select_music():
    if request.method == 'GET':
        # 가수 이름 - 앨범커버 교체 위한 변수
        singer = request.args.get('singer', 'iu')
        print('가수 : ' + singer)
        song_list = list()

        # 원본 가수
        # singer에 따라서 가능한 노래목록이 달라지도록 설정
        # 되는 것은 장범준 -> test곡제목 -> iu 시나리오만 되어있음
        # 새로운 노래를 추가할 경우 svc_select_music, svc_select_artist, svc, app을 모두 수정해야.
        if singer == 'jang' :
            song_list.append('test곡제목')
            song_list.append('test곡제목2')
        elif singer == 'iu' :
            song_list.append('test곡제목2')
            song_list.append('test곡제목3')
            song_list.append('test곡제목4')

        print("노래 목록 ")
        for i, song in enumerate(song_list):
            print(i,"번째 : ",song)
        return render_template('svc_select_music.html', singer=singer,song_list=song_list)
        # return redirect("https://url.kr/jFq9KO")

# singing voice conversion 메뉴
@app.route('/svc',methods = ['GET'])
def svc():
    if request.method == 'GET':
        # 원본 가수 이름
        singer = request.args.get('singer', 'iu')
        # title - 제목
        title = request.args.get('title', 'iu')
        # 바꿀 대상 가수
        target_singer = request.args.get('target_singer', 'iu')

        # 노래 제목에 따라 실제 재생할 파일 경로 설정
        if(title == 'test곡제목' ):
            file = 'na.wav'
        else:
            file = 'etc.wav'

        return render_template('svc.html', singer=singer,title=title,file=file,target_singer = target_singer)


@app.route('/tts',methods = ['GET'])
def tts():
    if request.method == 'GET':
        singer = request.args.get('singer','iu')
        return render_template('tts.html',singer=singer)


@app.route('/tts_result',methods = ['POST'])
def tts_result(display=None):
    if request.method == 'POST':
        if request.method == 'POST':
            text = request.form['tts-text']
            singer = request.form['singer']

            with open('tts_storage/text/tts_script.txt', 'w', encoding='utf-8') as file:
                newline_removed_string = text.replace('\n', "").strip()
                period_separated_lines = [line.strip() for line in newline_removed_string.split('.') if line]
                for line in period_separated_lines:
                    file.write(line + '.\n')
                file.close()
            print("## Creating Voice file...")
            textConv.generate_voice()
            print("## Voice Created.")
            print("## Voice Conversion Start...")
            t2s.converting('A2B')
            print("## Conversion Done")
            shutil.copy('./text_conversion/sample/tts.wav', './static/tts.wav')

        return render_template("tts_result.html", display=text,singer=singer,file_name='tts.wav')


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
@app.route('/download_sts',methods=['GET','POST'])
def download_sts():
    if request.method == 'POST' :
        # files = os.listdir('./tts_storage')
        path = './voice_conversion/sample/'
        # POST로 전달받은 파일이름을 이용하여 다운로드
        file_name = 'voice.wav'
        return send_file(path + file_name,
                         attachment_filename=file_name,
                         as_attachment=True)

# tts file download
@app.route('/download_tts',methods=['GET','POST'])
def download_tts():
    if request.method == 'POST' :
        # files = os.listdir('./tts_storage')
        path = './text_conversion/sample/'
        # POST로 전달받은 파일이름을 이용하여 다운로드
        file_name = 'tts.wav'
        return send_file(path + file_name,
                         attachment_filename=file_name,
                         as_attachment=True)

# 녹음 버튼 눌렀을 때
# 버튼을 한번누르면 넘어가는 state값이 ready -> recording으로 바뀐다
@app.route('/record',methods=['POST'])
def record():
    if request.method == 'POST' :
        data = request.get_json()
        voiceConv.speech_voice_conv()
        print('recording Done & Voice Converting Begin')
        s2s.converting()
        print('Converting Done')
        shutil.copy('./voice_conversion/sample/voice.wav', './static/voice.wav')
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

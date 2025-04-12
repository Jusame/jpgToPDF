from flask import Flask, render_template, request, jsonify, url_for
import os
import uuid
from pdf2image import convert_from_bytes  # pdf2image 라이브러리 사용 (poppler 설치 필요)
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 변환된 이미지 파일을 저장할 폴더 (static/downloads)
DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# ----------------------------------------------------------------------
# 1. 인덱스 페이지 렌더링 (GET 요청)
# ----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# ----------------------------------------------------------------------
# 2. PDF 업로드 및 JPG 변환 처리 (POST 요청)
# ----------------------------------------------------------------------
@app.route('/', methods=['POST'])
def convert_pdf_to_jpg():
    # 업로드된 파일이 존재하는지 확인
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'PDF 파일이 첨부되지 않았습니다.'}), 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400
    
    try:
        # 업로드된 PDF 파일을 바이트 단위로 읽기
        pdf_bytes = pdf_file.read()
        
        # pdf2image를 이용해 PDF를 이미지로 변환 (여기서는 첫 페이지만 변환)
        pages = convert_from_bytes(pdf_bytes, fmt='jpeg', first_page=1, last_page=1)
        if len(pages) == 0:
            return jsonify({'error': 'PDF 변환에 실패했습니다.'}), 500
        
        # 변환된 첫 페이지 이미지 선택
        image = pages[0]
        
        # 고유한 파일명 생성 (확장자는 .jpg)
        filename = f"converted_{uuid.uuid4().hex}.jpg"
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], secure_filename(filename))
        
        # 이미지 저장 (JPEG 형식)
        image.save(file_path, 'JPEG')
        
        # 저장된 파일을 다운로드할 수 있도록 URL 생성 (_external=True를 사용해 절대 경로 생성)
        download_url = url_for('static', filename=f"downloads/{filename}", _external=True)
        return jsonify({'download_url': download_url})
    
    except Exception as e:
        # 예외 발생 시 에러 메시지 반환
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------
# 3. 서버 실행
# ----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

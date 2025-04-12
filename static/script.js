document.addEventListener('DOMContentLoaded', function() {
  // 업로드 폼 요소 가져오기
  const form = document.getElementById('upload-form');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // 폼의 기본 제출 동작 막기

    // 결과를 표시할 영역 초기화
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    // 파일 입력에서 선택된 파일 확인
    const fileInput = document.getElementById('pdf-file');
    if (!fileInput.files.length) {
      resultDiv.innerHTML = '<p>파일을 선택해 주세요.</p>';
      return;
    }

    // FormData에 파일 추가
    const formData = new FormData();
    formData.append('pdf_file', fileInput.files[0]);

    // 제출 버튼 상태 변경 (중복 제출 방지)
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = '변환 중...';

    // fetch를 이용하여 비동기 POST 요청 전송
    fetch('/', {  // 서버의 URL은 Flask에서 라우팅한 엔드포인트에 맞게 조정
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('서버 응답이 좋지 않습니다.');
      }
      return response.json();
    })
    .then(data => {
      // 서버에서 download_url이 있으면 다운로드 링크를, error 메시지가 있으면 에러 메시지 표시
      if (data && data.download_url) {
        resultDiv.innerHTML = `<p>파일 변환이 완료되었습니다. <a href="${data.download_url}" download>여기를 클릭</a>하여 다운로드 하세요.</p>`;
      } else if (data && data.error) {
        resultDiv.innerHTML = `<p>오류가 발생했습니다: ${data.error}</p>`;
      } else {
        resultDiv.innerHTML = '<p>예상치 못한 서버 응답입니다.</p>';
      }
    })
    .catch(error => {
      resultDiv.innerHTML = `<p>오류가 발생했습니다: ${error.message}</p>`;
    })
    .finally(() => {
      // 요청 완료 후 버튼 원래 상태로 복원
      submitButton.disabled = false;
      submitButton.textContent = 'JPG로 변환';
    });
  });
});

const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const button = document.getElementById('capture-btn');

// Mở webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  });

button.addEventListener('click', () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);

  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append('image', blob, 'capture.jpg');

    resultDiv.innerText = '⏳ Đang phân tích...';

    fetch('/analyze', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        resultDiv.innerText = '✅ ' + data.label;
      })
      .catch(err => {
        resultDiv.innerText = '❌ Lỗi: ' + err.message;
      });
  }, 'image/jpeg');
});

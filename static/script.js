const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const captureBtn = document.getElementById('capture-btn');
const switchBtn = document.getElementById('switch-btn');

let currentFacingMode = 'environment'; // 'user' cho camera trước
let stream = null;

// Hàm khởi động camera
async function startCamera(facingMode = 'environment') {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: facingMode } },  // Ưu tiên dùng loại camera mong muốn
      audio: false
    });
    video.srcObject = stream;
  } catch (err) {
    console.error('Camera error:', err);
    resultDiv.innerText = '❌ Không thể truy cập camera: ' + err.message;
  }
}

// Bắt đầu camera với camera sau (mặc định)
startCamera(currentFacingMode);

// Chuyển camera khi nhấn nút
switchBtn.addEventListener('click', () => {
  currentFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
  startCamera(currentFacingMode);
});

// Chụp ảnh và gửi lên server
captureBtn.addEventListener('click', () => {
  if (!video.videoWidth || !video.videoHeight) {
    resultDiv.innerText = '❌ Không thể chụp ảnh: camera chưa sẵn sàng';
    return;
  }

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
        console.error('Fetch error:', err);
        resultDiv.innerText = '❌ Lỗi: ' + err.message;
      });
  }, 'image/jpeg');
});

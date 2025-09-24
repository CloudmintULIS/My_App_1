// --- Lấy phần tử ---
const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const previewImg = document.getElementById('preview-img');
const captureBtn = document.getElementById('capture-btn');
const switchBtn = document.getElementById('switch-btn');
const zoomSlider = document.getElementById('zoom-slider');
const zoomContainer = document.querySelector('.zoom-container');
const uploadInput = document.getElementById('upload-input');

let currentFacingMode = 'environment'; // mặc định camera sau
let stream = null;

// --- Hàm đọc to nhãn ---
function speakLabel(label) {
  if ('speechSynthesis' in window && 'SpeechSynthesisUtterance' in window) {
    const utterance = new SpeechSynthesisUtterance(label);
    utterance.lang = 'en-US';
    speechSynthesis.cancel(); // hủy giọng đọc cũ nếu có
    speechSynthesis.speak(utterance);
  }
}

// --- Khởi động camera ---
async function startCamera(facingMode = 'environment') {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }

  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(d => d.kind === 'videoinput');

    if (videoDevices.length === 0) {
      throw new Error("Không tìm thấy camera nào");
    }

    let constraints;
    if (videoDevices.length === 1) {
      constraints = { video: { deviceId: { exact: videoDevices[0].deviceId } }, audio: false };
    } else {
      constraints = { video: { facingMode: { ideal: facingMode } }, audio: false };
    }

    stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;

    // --- Zoom nếu hỗ trợ ---
    const [track] = stream.getVideoTracks();
    const capabilities = track.getCapabilities();

    if (videoDevices.length > 1 && 'zoom' in capabilities) {
      zoomContainer.style.display = 'block';
      zoomSlider.min = capabilities.zoom.min;
      zoomSlider.max = capabilities.zoom.max;
      zoomSlider.step = capabilities.zoom.step || 0.1;
      zoomSlider.value = capabilities.zoom.min;

      zoomSlider.oninput = () => {
        track.applyConstraints({ advanced: [{ zoom: zoomSlider.value }] });
      };
    } else {
      zoomContainer.style.display = 'none';
    }

  } catch (err) {
    console.error('Camera error:', err);
    resultDiv.innerText = "❌ Lỗi camera: " + err.message;
  }
}

// --- Bắt đầu camera mặc định ---
startCamera(currentFacingMode);

// --- Chuyển camera ---
switchBtn.addEventListener('click', () => {
  currentFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
  startCamera(currentFacingMode);
});

// --- Chụp ảnh ---
captureBtn.addEventListener('click', () => {
  if (!video.videoWidth || !video.videoHeight) {
    resultDiv.innerText = '❌ Camera chưa sẵn sàng';
    return;
  }

  // --- Resize canvas để gửi nhẹ hơn ---
  const MAX_WIDTH = 800;
  const scale = Math.min(MAX_WIDTH / video.videoWidth, 1);
  canvas.width = video.videoWidth * scale;
  canvas.height = video.videoHeight * scale;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append('image', blob, 'capture.jpg');

    resultDiv.innerText = '⏳ Đang phân tích...';

    // Hiển thị preview nhỏ góc video
    previewImg.src = URL.createObjectURL(blob);
    previewImg.style.display = 'block';

    fetch('/analyze', { method: 'POST', body: formData })
      .then(res => res.json())
      .then(data => {
        const label = data.label;
        resultDiv.innerHTML = `✅ <b>${label}</b>`;
        speakLabel(label);
      })
      .catch(err => {
        console.error('Fetch error:', err);
        resultDiv.innerText = '❌ Lỗi: ' + err.message;
      });
  }, 'image/jpeg');
});

// --- Upload ảnh ---
uploadInput.addEventListener('change', () => {
  if (uploadInput.files.length === 0) return;

  const file = uploadInput.files[0];
  const formData = new FormData();
  formData.append('image', file, file.name);

  resultDiv.innerText = '⏳ Đang phân tích...';

  // Hiển thị preview nhỏ góc video
  previewImg.src = URL.createObjectURL(file);
  previewImg.style.display = 'block';

  fetch('/analyze', { method: 'POST', body: formData })
    .then(res => res.json())
    .then(data => {
      const label = data.label;
      resultDiv.innerHTML = `✅ <b>${label}</b>`;
      speakLabel(label);
    })
    .catch(err => {
      console.error('Upload error:', err);
      resultDiv.innerText = '❌ Lỗi: ' + err.message;
    });
});

const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const resultDiv = document.getElementById('result');
const captureBtn = document.getElementById('capture-btn');
const switchBtn = document.getElementById('switch-btn');
const zoomSlider = document.getElementById('zoom-slider');
const zoomContainer = document.querySelector('.zoom-container');

let currentFacingMode = 'environment'; // mặc định camera sau
let stream = null;

// Hàm khởi động camera
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
      // ✅ Laptop chỉ có 1 camera → chọn đúng deviceId
      constraints = {
        video: { deviceId: { exact: videoDevices[0].deviceId } },
        audio: false
      };
    } else {
      // ✅ Mobile có nhiều camera → dùng facingMode
      constraints = {
        video: { facingMode: { ideal: facingMode } },
        audio: false
      };
    }

    stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;

    // --- Zoom chỉ khi mobile có nhiều camera ---
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

    if (err.name === "NotReadableError") {
      resultDiv.innerText = "❌ Camera đang bận. Hãy tắt ứng dụng khác (Zoom, Camera app, OBS...) rồi thử lại.";
    } else if (err.name === "NotAllowedError") {
      resultDiv.innerText = "❌ Truy cập camera bị chặn. Hãy cấp quyền trong trình duyệt.";
    } else if (err.name === "NotFoundError") {
      resultDiv.innerText = "❌ Không tìm thấy camera nào.";
    } else {
      resultDiv.innerText = "❌ Không thể truy cập camera: " + err.message;
    }
  }
}

// Bắt đầu camera mặc định
startCamera(currentFacingMode);

// Nút chuyển camera
switchBtn.addEventListener('click', () => {
  currentFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
  startCamera(currentFacingMode);
});

// Nút chụp ảnh
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
        const label = data.label;
        const wordInfo = data.word_info || {};

        let html = `✅ <b>${label}</b>`;
        resultDiv.innerHTML = html;

        // TTS đọc từ
        if ('speechSynthesis' in window && 'SpeechSynthesisUtterance' in window) {
          const utterance = new SpeechSynthesisUtterance(label);
          utterance.lang = 'en-US';
          speechSynthesis.speak(utterance);
        }
      })
      .catch(err => {
        console.error('Fetch error:', err);
        resultDiv.innerText = '❌ Lỗi: ' + err.message;
      });
  }, 'image/jpeg');
});

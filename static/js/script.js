const button = document.getElementById('ler-charada');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const stopButton = document.getElementById('parar-camera');

// Evento para iniciar a câmera e o processo de leitura
button.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then((stream) => {
            video.srcObject = stream;
            video.setAttribute('playsinline', true); // Requisito para iOS
            video.style.display = 'block';
            stopButton.style.display = 'block';
            video.play();

            // Garante que o vídeo esteja carregado antes de começar a leitura
            video.addEventListener('loadedmetadata', () => {
                scan(); // Inicia o processo de escaneamento
            });
        })
        .catch((err) => {
            console.error("Erro ao acessar a câmera:", err);
            alert("Não foi possível acessar a câmera. Verifique as permissões.");
        });
});

// Evento para parar a câmera
stopButton.addEventListener('click', () => {
    pararCamera();
});

// Função para escanear o QR Code
function scan() {
    if (video.videoWidth > 0 && video.videoHeight > 0) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code && code.data) {
            alert(`Charada detectada: ${code.data}`);

            // Parar a câmera e ocultar elementos
            pararCamera();

            // Tratamento para extrair o ID da URL do QR Code
            const url = new URL(code.data.trim());
            const id = url.pathname.split('/').pop(); // Obtém o último segmento da URL (ID)

            if (id && !isNaN(parseInt(id))) {
                window.location.href = `/charada/${id}`;
            } else {
                alert("QR Code inválido! Certifique-se de que o código contém um ID válido.");
            }
        } else {
            requestAnimationFrame(scan);
        }
    } else {
        setTimeout(scan, 100);
    }
}

// Função para parar a câmera
function pararCamera() {
    const stream = video.srcObject;
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
    }
    video.style.display = 'none';
    stopButton.style.display = 'none';
}

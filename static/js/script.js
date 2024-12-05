const button = document.getElementById('ler-charada');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

button.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then((stream) => {
            video.srcObject = stream;
            video.setAttribute('playsinline', true);
            video.style.display = 'block';
            video.play();
            scan();  // Inicia o processo de leitura assim que o vídeo começa a ser exibido
        })
        .catch((err) => {
            console.error("Erro ao acessar a câmera:", err);
            alert("Não foi possível acessar a câmera.");
        });
});

const stopButton = document.getElementById('parar-camera');

stopButton.addEventListener('click', () => {
    const stream = video.srcObject;
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.style.display = 'none';
        stopButton.style.display = 'none';
    }
});

function scan() {
    // Verifica se o vídeo tem dimensões válidas (largura e altura)
    if (video.videoWidth > 0 && video.videoHeight > 0) {
        // Define o tamanho do canvas baseado no tamanho do vídeo
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Desenha o quadro atual do vídeo no canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code) {
            alert(`Charada detectada: ${code.data}`);
            window.location.href = `/charada/${code.data}`;
        } else {
            requestAnimationFrame(scan); // Reexecuta o scan se o QR code não for encontrado
        }
    } else {
        // Se o vídeo ainda não estiver pronto, tenta novamente
        requestAnimationFrame(scan);
    }
}

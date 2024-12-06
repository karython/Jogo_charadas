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
            video.setAttribute('playsinline', true);
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
            alert("Não foi possível acessar a câmera.");
        });
});

// Evento para parar a câmera
stopButton.addEventListener('click', () => {
    const stream = video.srcObject;
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.style.display = 'none';
        stopButton.style.display = 'none';
    }
});

// Função para escanear o QR Code
function scan() {
    // Verifica se o vídeo tem dimensões válidas
    if (video.videoWidth > 0 && video.videoHeight > 0) {
        // Define o tamanho do canvas baseado no vídeo
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Desenha o quadro atual do vídeo no canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Obtém os dados da imagem do canvas
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

        // Usa a biblioteca jsQR para ler o QR Code
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code && code.data) {
            // QR Code detectado
            alert(`Charada detectada: ${code.data}`);
            window.location.href = `/charada/${code.data}`;
        } else {
            // Continua tentando se o QR Code não for detectado
            requestAnimationFrame(scan);
        }
    } else {
        // Reexecuta a leitura até que o vídeo esteja pronto
        setTimeout(scan, 100);
    }
}

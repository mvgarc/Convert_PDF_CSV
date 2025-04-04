document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    
    let fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Por favor, selecciona un archivo PDF.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    let message = document.getElementById("message");
    let downloadLink = document.getElementById("downloadLink");

    message.textContent = "Procesando...";
    downloadLink.style.display = "none";

    try {
        let response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            let blob = await response.blob();
            let url = window.URL.createObjectURL(blob);
            downloadLink.href = url;
            downloadLink.download = "archivo_convertido.csv";
            downloadLink.textContent = "Descargar CSV";
            downloadLink.style.display = "block";
            message.textContent = "Conversión exitosa.";
        } else {
            let errorData = await response.json();
            message.textContent = "Error: " + errorData.error;
        }
    } catch (error) {
        message.textContent = "Error al conectar con el servidor.";
    }
});

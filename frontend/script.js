document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Por favor, selecciona un archivo.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const message = document.getElementById("message");
    const downloadLink = document.getElementById("downloadLink");

    message.textContent = "Procesando...";
    downloadLink.style.display = "none";

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            message.textContent = "Error: " + errorData.error;
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        downloadLink.href = url;
        downloadLink.download = "resultado.csv";  
        downloadLink.textContent = "Descargar CSV";
        downloadLink.style.display = "block";

        message.textContent = "Conversión exitosa.";
    } catch (error) {
        message.textContent = "Error al conectar con el servidor.";
        console.error(error);
    }
});

document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const message = document.getElementById("message");
    const downloadLink = document.getElementById("downloadLink");

    if (!fileInput.files.length) {
        alert("Por favor, selecciona un archivo.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

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

        // Descargar automáticamente el archivo CSV
        const a = document.createElement("a");
        a.href = url;
        a.download = "archivo_procesado.csv"; 
        document.body.appendChild(a);
        a.click();
        a.remove();

        // También dejar opción de descarga manual
        downloadLink.href = url;
        downloadLink.download = "archivo_procesado.csv";
        downloadLink.textContent = "Descargar CSV";
        downloadLink.style.display = "block";

        message.textContent = "Conversión exitosa.";
    } catch (error) {
        message.textContent = "Error al conectar con el servidor.";
        console.error(error);
    }
});

// Mostrar el nombre del archivo seleccionado
document.getElementById("fileInput").addEventListener("change", function () {
    const fileName = this.files[0] ? this.files[0].name : "Ningún archivo seleccionado";
    document.getElementById("fileName").textContent = fileName;
});

// frontend/JS/index.js

function uploadFile() {
  const input = document.getElementById("csvFileInput");
  const file = input.files[0];
  const formData = new FormData();

  formData.append("csvFile", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("File uploaded successfully.");
        // Call backend to start data processing (You can use WebSocket or polling for progress).
        // Implement logic to show loading indicator while processing.
      } else {
        alert("File upload failed.");
      }
    })
    .catch((error) => {
      console.error("Error uploading file:", error);
    });
}

// Update the label text with the selected file name
document.getElementById("csvFileInput").addEventListener("change", function () {
  const inputLabel = document.getElementById("fileInputLabel");
  const file = this.files[0];
  if (file) {
    inputLabel.innerText = file.name;
  } else {
    inputLabel.innerText = "Select a CSV file...";
  }
});

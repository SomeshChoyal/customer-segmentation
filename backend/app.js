const express = require("express");
const multer = require("multer");
const path = require("path");
const cors = require("cors");
const { PythonShell } = require("python-shell");

const app = express();
const port = 3000;

// Enable CORS for all routes
app.use(
  cors({
    origin: "http://127.0.0.1:5500/frontend/index.html", // Replace this with the actual URL of your frontend
  })
);

app.use(express.static(path.join(__dirname, "public")));

// Configure multer for file upload
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, "uploads")); // Use path.join to create the correct destination path
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });

// Handle POST request to upload the file and perform K-means clustering
app.post("/upload", upload.single("csvFile"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  // Path to the Python executable
  const pythonPath =
    "C:/Users/Somesh Choyal/AppData/Local/Programs/Python/Python310/python.exe"; // Adjust the path accordingly

  // Path to the kmeans.py script
  const pythonScriptPath = path.join(__dirname, "kmeans.py"); // Adjust the path accordingly

  // Execute the kmeans.py script
  const options = {
    mode: "text",
    pythonOptions: ["-u", pythonPath], // unbuffered output and Python executable path
    scriptPath: __dirname, // Path to the directory containing kmeans.py
    args: [req.file.path], // Pass the file path as an argument to the Python script
  };

  PythonShell.run("kmeans.py", options, (err, results) => {
    if (err) {
      console.error("Python script execution error:", err);
      return res.status(500).send("An error occurred during clustering.");
    }

    // Process the clustering results returned by the Python script
    console.log("Clustering results:", results);

    // Send the clustering results back to the frontend (you may want to format the results as needed)
    res.status(200).send(results);
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

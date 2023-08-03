const express = require("express");
const multer = require("multer");
const path = require("path");
const { exec } = require("child_process");
const app = express();
const fs = require("fs");
const { spawn } = require("child_process");
const cors = require("cors");

// Rest of your code...
app.use(cors());
// Set up the destination and filename options for multer
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "C:\\Users\\Somesh Choyal\\Desktop\\New folder\\backend\\upload");
  },
  filename: function (req, file, cb) {
    const timestamp = Date.now();
    const originalName = file.originalname;
    const fileName = `uploaded-${timestamp}-${originalName}`;
    cb(null, fileName);
  },
});

const upload = multer({ storage: storage });

app.post("/upload", upload.single("csvFile"), (req, res) => {
  // Process the uploaded file here if needed (e.g., move, rename, etc.).
  // For simplicity, we won't process the file further in this example.

  // Get the uploaded file location
  const fileLocation = req.file.path;

  // Call the Python script with the uploaded file location as an argument
  const processScript = path.join(__dirname, "data-processing.py");
  const command = `python "${processScript}" "${fileLocation}"`;

  // Inside the app.post("/upload") route handler...

exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error("Error:", error.message);
    return res.status(500).send("Error processing data.");
  } else if (stderr) {
    console.error("Error:", stderr);
    return res.status(500).send("Error processing data.");
  } else {
    // Process the Python script output to get the processed file path
    const processedFilePath = stdout.trim();

    // Call the K-means function with the processed file path
    console.log(processedFilePath);
    const outputFolder = "C:\\Users\\Somesh Choyal\\Desktop\\New folder\\backend\\output";
    runKMeansClustering(processedFilePath, outputFolder);

    // Respond with success status
    res.sendStatus(200);
  }
});
// Inside the app.post("/upload") route handler...

// Send the list of available clusters and their file names to the frontend
app.get("/clusters", (req, res) => {
  const outputFolder = "C:\\Users\\Somesh Choyal\\Desktop\\New folder\\backend\\output";
  const clusterFiles = fs.readdirSync(outputFolder)
    .filter(file => file.endsWith(".csv"))
    .map(file => ({ clusterId: file.split("_")[1].split(".")[0], fileName: file }));

  res.json(clusterFiles);
});

});
// Inside the app.post("/upload") route handler...

// Send the list of available clusters and their file names to the frontend
app.get("/clusters", (req, res) => {
  const outputFolder = "C:\\Users\\Somesh Choyal\\Desktop\\New folder\\backend\\output";
  const clusterFiles = fs.readdirSync(outputFolder)
    .filter(file => file.endsWith(".csv"))
    .map(file => ({ clusterId: file.split("_")[1].split(".")[0], fileName: file }));

  res.json(clusterFiles);
});

// Add a new route to handle the download request
app.get("/download/:clusterId", (req, res) => {
  const outputFolder = "C:\\Users\\Somesh Choyal\\Desktop\\New folder\\backend\\output";
  const clusterId = req.params.clusterId;
  const fileName = `Cluster_${clusterId}.csv`;
  const filePath = path.join(outputFolder, fileName);

  // Send the file as a download attachment
  res.download(filePath);
});


// ...

function runKMeansClustering(csvFilePath, outputFolder) {
  const pythonScript =
    "C:\\Users\\Somesh Choyal\\Desktop\\New folder\\backend\\kmeans.py";

  // Arguments to pass to the Python script
  const args = [pythonScript, csvFilePath, outputFolder];

  // Execute the Python script
  const pythonProcess = spawn("python", args);

  // Log the output of the Python script
  pythonProcess.stdout.on("data", (data) => {
    console.log(data.toString());
  });

  // Log any errors from the Python script
  pythonProcess.stderr.on("data", (data) => {
    console.error(data.toString());
  });

  // Log when the Python script execution is completed
  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
  });
}




// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

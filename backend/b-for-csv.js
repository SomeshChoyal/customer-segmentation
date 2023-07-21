const express = require("express");
const multer = require("multer");
const csv = require("csv-parser");
const fs = require("fs");
const path = require("path");
const cors = require("cors");

const app = express();
const port = 3000;

// Enable CORS for all routes and specify the allowed origin
app.use(
  cors({
    origin: "http://127.0.0.1:5500", // Replace this with the actual URL of your frontend
  })
);

// Serve static files from the "public" directory
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

// Handle POST request to upload the file
app.post("/upload", upload.single("csvFile"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  const results = [];
  fs.createReadStream(req.file.path)
    .pipe(csv())
    .on("data", (data) => results.push(data))
    .on("end", () => {
      // Process the CSV data here (you can save it to a database or perform any other operations)
      console.log(results);
      res.sendStatus(200); // Sending a success status back to the frontend
    });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

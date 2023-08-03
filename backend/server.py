# server.py

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'backend/input-csv'
PROCESSED_FOLDER = 'backend/output-csv'


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['csvFile']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Call the data processing function
        output_file_path = os.path.join(
            PROCESSED_FOLDER, 'processed_' + file.filename)
        process_data(file_path, output_file_path)

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


if __name__ == '__main__':
    app.run(debug=True)

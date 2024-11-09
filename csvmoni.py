from flask import Flask, render_template, request, send_file
import pandas as pd
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file from the request
        file = request.files['file']

        # Generate the one-hot encoded CSV file
        output_path = 'encoded_output.csv'
        generate_one_hot_encoded_csv(file, output_path)

        # Return the encoded CSV file for download
        return send_file(output_path, as_attachment=True)

    return render_template('index.html')

def generate_one_hot_encoded_csv(input_file, output_path):
    # Load original data
    data = pd.read_csv(input_file)

    # Extract tasting notes columns with corrected names
    sample_1_notes = data['Sample 1 '].str.split(', ')
    sample_2_notes = data['Sample 2'].str.split(', ')

    # Collect all unique tasting descriptors from both samples
    unique_descriptors = set()
    for notes in sample_1_notes.dropna().tolist() + sample_2_notes.dropna().tolist():
        unique_descriptors.update(notes)
    unique_descriptors = sorted(unique_descriptors)  # Sort descriptors for consistency

    # Create a new DataFrame for the encoded format
    encoded_data = []
    for i, row in data.iterrows():
        for sample_num, sample_key in zip(['A', 'B'], ['Sample 1 ', 'Sample 2']):
            encoded_row = {'N Muestra': i + 1, '': sample_num}
            notes = row[sample_key].split(', ') if pd.notna(row[sample_key]) else []
            # One-hot encode each descriptor using integers instead of floats
            for descriptor in unique_descriptors:
                encoded_row[descriptor] = 1 if descriptor in notes else 0
            encoded_data.append(encoded_row)

    # Convert to DataFrame and save to CSV
    encoded_df = pd.DataFrame(encoded_data)
    encoded_df.to_csv(output_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

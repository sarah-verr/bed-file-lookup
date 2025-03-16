# BED File Lookup Service

This project provides a simple web service to compare BED files based on the Jaccard index.

## Features

- Upload a BED file
- Compare with stored database files
- Return the most similar files using Jaccard similarity

## Setup

### Running Locally

1. Clone the repository:
   ```sh
   git clone https://github.com/sarah-verr/bed-file-lookup
   cd bed-file-lookup
   ```
2. Install dependencies:
   ```sh
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   ```
   3. Ensure you have the database BED files downloaded or generated. Check if they exist using:
   ```sh
   ls *.bed
   ```
   If they are missing, download or create them first. Then, store them in a `database/` directory:
   ```sh
   mkdir database
   mv ENCFF082UWB.bed ENCFF190KNC.bed ENCFF247CME.bed ENCFF608BGQ.bed ENCFF832YGL.bed database/
   ```
4. Run the server:
   ```sh
   uvicorn main:app --reload
   ```
5. Open [localhost:8000](http://localhost:8000) in a browser.

### Running with Docker

1. Build the Docker image:
   ```sh
   docker build -t bed_lookup .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 bed_lookup
   ```
3. Open [localhost:8000](http://localhost:8000) in a browser.

## API

- `POST /upload/` - Upload a BED file and get similarity results.
  - **Request**: Multipart form with `file` (BED format) and `top_n` (integer, default = 3)
  - **Response**: JSON with top matching database files sorted by Jaccard similarity.

## Example Usage

You can test the API using `curl`:

```sh
curl -X POST "http://localhost:8000/upload/" \
     -F "file=@test.bed" \
     -F "top_n=3"
```

## Requirements

- Python 3.9+
- Dependencies from `requirements.txt` (FastAPI, Uvicorn, PyBedTools)

## Notes

- Ensure the database BED files are formatted correctly.
- The service computes Jaccard similarity between uploaded files and database files.


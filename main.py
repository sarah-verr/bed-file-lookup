from fastapi import FastAPI, File, UploadFile
import pybedtools
import tempfile
import os
import glob
from fastapi.responses import HTMLResponse

app = FastAPI()

db_directory = "database/"  # Directory containing the core BED files

def compute_jaccard(file1: str, file2: str) -> float:
    """Compute Jaccard index between two BED files."""
    a = pybedtools.BedTool(file1)
    b = pybedtools.BedTool(file2)
    
    intersection = a.intersect(b, u=True)
    union = a.cat(b, postmerge=False)
    
    intersection_size = sum(len(i) for i in intersection)
    union_size = sum(len(i) for i in union)
    
    if union_size == 0:
        return 0.0
    return intersection_size / union_size

@app.post("/upload/")
async def upload_bed(file: UploadFile = File(...), top_n: int = 3):
    """Endpoint to upload a BED file and find the most similar database files."""
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name
    
    results = []
    for db_file in glob.glob(os.path.join(db_directory, "*.bed")):
        jaccard_score = compute_jaccard(temp_file_path, db_file)
        results.append((os.path.basename(db_file), jaccard_score))
    
    os.remove(temp_file_path)
    
    results.sort(key=lambda x: x[1], reverse=True)
    return {"top_matches": results[:top_n]}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h2>BED File Lookup</h2>
            <form action="/upload/" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="number" name="top_n" value="3" min="1">
                <button type="submit">Upload</button>
            </form>
        </body>
    </html>
    """


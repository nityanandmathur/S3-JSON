# S3-JSON

## Pre-req.
```bash
pip install boto3
pip install awscli

aws configure
```

## Usage
Update `BUCKET_NAME` and `FILE_KEY` in the python file.
```bash
python s3_json.py
```
## Exporting as an standalone desktop application
```bash
pip install pyinstaller

pyinstaller --windowed s3_json.py
```

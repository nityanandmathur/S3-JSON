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
> Double click on the values to see them in a new window.

## Exporting as an standalone desktop application
```bash
pip install pyinstaller

pyinstaller --windowed s3_json.py
```

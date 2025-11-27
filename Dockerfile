FROM python:3.10

WORKDIR /code

# Install dependencies from root-level requirements.txt
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files (main.py, model.pkl, scaler.pkl, etc.)
COPY . /code/

# Expose Hugging Face default port
EXPOSE 7860

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

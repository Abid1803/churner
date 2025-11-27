FROM python:3.10

WORKDIR /code

# Copy and install dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files into container
COPY . /code/

# Hugging Face uses port 7860
EXPOSE 7860

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

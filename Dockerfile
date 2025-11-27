FROM python:3.10

# Working directory inside container
WORKDIR /code

# Install Python dependencies from backend folder
COPY backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files into container
COPY backend /code/

# Expose Hugging Face default port
EXPOSE 7860

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

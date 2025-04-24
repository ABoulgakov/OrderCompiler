# 1. Use an official Python image
FROM python:3.10-slim

# 2. Set working directory in the container
WORKDIR /app

# 3. Copy the requirements.txt file into the image
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the app's code
COPY . .

# 6. Expose the Streamlit port
EXPOSE 8501

# 7. Run Streamlit when the container starts
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

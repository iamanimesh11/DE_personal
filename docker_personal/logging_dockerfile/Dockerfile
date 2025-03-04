# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only the Python scripts
COPY python_Files/ /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports (only if the script runs a web UI like Streamlit)
EXPOSE 8501

# Run the Python script
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

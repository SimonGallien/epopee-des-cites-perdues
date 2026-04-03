FROM python:3.14-slim
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
COPY scripts ./scripts
COPY data ./data
COPY main.py ./
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python3", "main.py"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY deployment_requirements.txt .
RUN pip install --no-cache-dir -r deployment_requirements.txt

# Copy the application code
COPY . .

# Streamlit configuration for deployment
RUN mkdir -p /root/.streamlit
RUN echo "\
[server]\n\
headless = true\n\
port = 5000\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
" > /root/.streamlit/config.toml

# Expose the port Streamlit runs on
EXPOSE 5000

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
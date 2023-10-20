# Pull base image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /server

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Initialize db and load fixtures
RUN python manage.py migrate && \
    python manage.py loaddata plants/fixtures/plants.json && \
    python manage.py loaddata plants/fixtures/diseases.json

CMD ["python", "/server/manage.py", "runserver", "0.0.0.0:8000"]
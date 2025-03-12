
FROM python:3.10-slim


WORKDIR /app

# Copy the app src code into the container workdir
COPY src /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any required Python dependencies
RUN pip install flask

# Expose port 5000 (the default port for Flask)
EXPOSE 5000

# Set environment variable for Flask to run in production
ENV FLASK_APP=stretchyagent.py
ENV FLASK_RUN_HOST=0.0.0.0

# If gunicorn will be used
# RUN pip install gunicorn

# Command to run the Flask application when the container starts (without gunicorn)
CMD ["flask", "run"]

# If guncorn used
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "stretchyapp:app"]


##
#


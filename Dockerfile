# Use an official Python runtime as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app
RUN apt update 

COPY . .


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run the command to start your application
CMD ["flask",  "--app",  "./backend/main",  "run", "--host",  "0.0.0.0"]
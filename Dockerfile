# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
RUN pip install django

# Start a shell to work within the container
CMD ["bash"]
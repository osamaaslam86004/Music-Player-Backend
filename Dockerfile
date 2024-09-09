# Step 1: Use an official Python runtime as a parent image
FROM python:3.9.20-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY ./requirements.txt /app/requirements.txt

# Step 4: Install any needed dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . /app

# Step 6: Expose the port that the FastAPI app will run on (default: 8000)
EXPOSE 8000

# Step 7: Set the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

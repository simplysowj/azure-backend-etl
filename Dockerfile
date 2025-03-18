# Step 1: Use the official Python image as a base
#FROM python:3.11-slim

# Step 2: Set the working directory inside the container
#WORKDIR /app

# Step 3: Copy the backend code into the container

#COPY backend/apiview/orm1/requirements.txt /app/requirements.txt
# Step 4: Install dependencies from requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the backend code into the container
#COPY backend/apiview/orm1 /app

# Step 6: Expose port 8000 for the Django app
#EXPOSE 8000

# Step 7: Set environment variables for Python
#ENV PYTHONUNBUFFERED=1

# Step 8: Run Django migrations and start the app
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "orm1.wsgi:application"]

FROM python:3.10-slim 

 

WORKDIR /app 

 

COPY requirements.txt /app/ 

RUN pip install --no-cache-dir -r requirements.txt 

 

COPY . /app/ 

 

ENV PYTHONDONTWRITEBYTECODE=1 

ENV PYTHONUNBUFFERED=1 

 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 

 


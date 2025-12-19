#base image
FROM python:3.13.2-slim



#working directory
WORKDIR /app

#copy
COPY . /app


#run  
RUN pip install -r requirements.txt

#port
EXPOSE  8000

#command
CMD ["python","./app.py"]

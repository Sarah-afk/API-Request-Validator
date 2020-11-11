FROM python:3.6
WORKDIR /project
ADD . /project 
RUN pip install -r requirements.txt
CMD python run.py

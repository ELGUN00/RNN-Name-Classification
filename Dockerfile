FROM python:3

WORKDIR /course_project

COPY . .

# RUN pip install --no-cache-dir -r req.txt
RUN pip install pandas
RUN pip install numpy
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install streamlit
RUN pip install torch



FROM python:3.13

WORKDIR /backend

COPY . /backend/

RUN pip3 install python-multipart
RUN pip3 install pyjwt[crypto]
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "src.main:app", "--reload", "--port=8000", "--host=0.0.0.0"]
EXPOSE 8000
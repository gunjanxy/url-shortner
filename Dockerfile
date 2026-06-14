#builder
FROM python:3.11-slim as builder
WORKDIR /home/app/
COPY requirements.txt .
RUN pip install -r requirements.txt
#final
FROM python:3.11-slim 
WORKDIR /home/app/
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/ 
COPY . .
CMD ["python","-u","app.py"]
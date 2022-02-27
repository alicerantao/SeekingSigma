FROM python:3

COPY . /run

WORKDIR /run

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python", "run.py" ]
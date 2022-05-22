FROM python:3.9

ARG APPLICATION_NAME=${APPLICATION_NAME}
ARG REQUIREMENTS=${REQUIREMENTS}

ENV APPLICATION_NAME ${APPLICATION_NAME}

COPY . /run

WORKDIR /run

RUN cd /run

COPY ${REQUIREMENTS} requirements.txt
RUN pip3 install -r requirements.txt

# ENTRYPOINT [ "python3", "api.py" ]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
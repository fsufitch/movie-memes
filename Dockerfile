FROM python:3.8 AS requirements-generator

WORKDIR /opt

RUN pip install --no-cache-dir -U 'pip>=21,<22'
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock /opt/
RUN echo "Locking requirements.txt:" && \
    poetry export -n | tee requirements.txt

##############################

FROM python:3.8 AS preprocessor

WORKDIR /opt/moviememes

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -U 'pip>=21,<22'

COPY --from=requirements-generator /opt/requirements.txt /opt/moviememes/
RUN echo "Installing requirements:" && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

COPY moviememes /opt/moviememes/moviememes
ENTRYPOINT [ "python", "-m", "moviememes.preprocessor.main" ]

##############################

FROM amazon/aws-lambda-python:3.8 as lambda 

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir -U 'pip>=21,<22'
COPY --from=requirements-generator /opt/requirements.txt .
RUN echo "Installing requirements:" && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

COPY moviememes ./moviememes
COPY lambda_entrypoint.py .

ENV MOVIE_DB_URL ${MOVIE_DB_URL}

CMD [ "lambda_entrypoint.main_handler" ] 
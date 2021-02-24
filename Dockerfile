FROM python:3.8 AS base

WORKDIR /opt/moviememes

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -U 'pip>=21,<22' poetry

COPY pyproject.toml poetry.lock /opt/moviememes/
RUN echo "Locking and installing requirements:" && \
    poetry export -n | tee requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

COPY moviememes /opt/moviememes/moviememes

FROM base AS preprocessor

ENTRYPOINT [ "python", "-m", "moviememes.preprocessor.main" ]
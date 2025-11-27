FROM python:3.10-slim
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential git \
&& pip install --no-cache-dir -r /app/requirements.txt \
&& apt-get remove -y build-essential git \
&& apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
COPY app /app
CMD ["python", "server.py"]
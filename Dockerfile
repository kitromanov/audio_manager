FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PATH="/usr/local/bin/aws:${PATH}"

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN mkdir -p /root/.aws \
    && echo "[default]" > /root/.aws/credentials \
    && echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}" >> /root/.aws/credentials \
    && echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}" >> /root/.aws/credentials

CMD ["python", "audio_manager/manage.py", "runserver", "0.0.0.0:8000"]

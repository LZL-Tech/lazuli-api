FROM python:3.9

RUN mkdir /opt/app
WORKDIR /opt/app

COPY requirements.txt ./
COPY . .

ENV ACCEPT_EULA=Y
RUN apt-get update
RUN apt-get install -y curl

RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null

RUN apt-get update
RUN apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN apt-get update

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "./app.py"]
FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN apt install unixodbc-dev

EXPOSE 5000

CMD ["python", "./app.py"]
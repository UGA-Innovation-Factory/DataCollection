FROM python:3

LABEL maintainer="Tomas Letelier"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY rtde/ ./rtde/
COPY UR10_reader.py .
COPY FakeUR10_reader.py .
COPY HiveMQConnect.py .
COPY UR10Output.txt .

ENV RUNFILE=UR10_reader.py

CMD python -u ${RUNFILE}
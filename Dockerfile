FROM python:3

WORKDIR /tmp

COPY docker/requirements.txt ./
COPY docker/hhparce.py ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=hhparce.py
ENV FLASK_ENV=development

CMD [ "flask", "run", "--host=0.0.0.0" ]
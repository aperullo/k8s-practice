from python:3.6-alpine as base
from base as builder

#Get dependencies
COPY ./requirements.txt /
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

# Set python path to include dependencies and src code
ENV PYTHONPATH=/src:/install/lib/python3.6/site-packages:$PYTHONPATH

COPY app.py /src/app.py
RUN dos2unix /src/*
RUN chmod 755 /src/*.py

FROM base

COPY --from=builder /install /usr/local
COPY --from=builder /src/app.py /app/
RUN ln -s /app/app.py /usr/local/bin/app.py
RUN chmod 755 /usr/local/bin/app.py

#tell flask what to run
RUN export FLASK_APP=/usr/local/bin/app.py

#expose flask's default port
EXPOSE 5000

#run the app
CMD ["flask", "run", "--host=0.0.0.0"]

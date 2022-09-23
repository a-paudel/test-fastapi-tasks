FROM python:slim

ENV PYTHONUNBUFFERED=1
# workdir
WORKDIR /app
# pipenv
RUN pip install pipenv
# install dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
# RUN pipenv install

# copy project
COPY . .

# prisma generate
# RUN pipenv run prisma generate
RUN prisma generate
# RUN pipenv run prisma db push

# run
CMD exec uvicorn server.app:app --host "0.0.0.0" --port $PORT
# CMD exec pipenv run server
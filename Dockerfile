FROM python:3.6.7

WORKDIR /app

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements_readthedocs.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app
RUN find .
RUN python setup.py install --user
EXPOSE 8000
CMD ["python", "testproject/manage.py", "runserver", "0.0.0.0:8000"]

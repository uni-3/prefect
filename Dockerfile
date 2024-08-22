FROM prefecthq/prefect:2-python3.11

#COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows

# Run our flow script when the container starts
#CMD ["python", "flows/prefect-docker-guide-flow.py"]
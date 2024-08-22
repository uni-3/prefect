FROM prefecthq/prefect:2-python3.11

#COPY requirements.txt .
#RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN pip install pandas airbyte>=0.15.0 prefect prefect_dbt python-dotenv

COPY flows /opt/prefect/flows

# Run our flow script when the container starts
#CMD ["python", "flows/prefect-docker-guide-flow.py"]
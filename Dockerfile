FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev build-essential && \
    apt-get clean

# Set the working directory
WORKDIR /usr/src/dbt/dbt_project

# Copy the dbt project files
COPY ./dbt_from_scratch/dbt_project /usr/src/dbt/dbt_project
COPY ./dbt_from_scratch/app/requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install dbt-postgres==1.3.1 && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the dbt profiles.yml
COPY ./dbt_from_scratch/profiles.yml /root/.dbt/profiles.yml

# Check dbt_project.yml
RUN cat /usr/src/dbt/dbt_project/dbt_project.yml

# Install dbt dependencies and build the project
CMD dbt deps && dbt build --profiles-dir /root/.dbt && sleep infinity

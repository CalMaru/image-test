FROM python:3.9.5

ENV HOME /image_test
RUN mkdir -p ${HOME}
WORKDIR ${HOME}

RUN apt-get update -y && apt-get install -y poppler-utils\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Dependencies
RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml ${HOME}
RUN poetry lock --no-update && poetry install --only main --no-root

# Copy Code
COPY . ${HOME}
RUN chmod -R 755 ${HOME}/entrypoint.sh

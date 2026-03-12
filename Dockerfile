FROM python:3.12-slim

# Installiamo curl
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Installiamo uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Aggiungiamo uv al PATH corretto
ENV PATH="/root/.local/bin:$PATH"

# Directory di lavoro
WORKDIR /app

COPY pyproject.toml .
# Installiamo Flask
# RUN uv pip install --system flask

RUN uv pip install --system --no-cache -r pyproject.toml

# Copiamo il progetto
COPY . .


# Avvio
CMD ["/bin/bash", "docker-entrypoint.sh"]
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
# ["flask", "run", "--host", "0.0.0.0"]
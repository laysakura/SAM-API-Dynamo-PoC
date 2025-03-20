FROM python:3.13-slim

WORKDIR /app

# Install AWS SAM CLI and AWS CLI
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl -Lo /tmp/aws-sam-cli.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-arm64.zip && \
    unzip /tmp/aws-sam-cli.zip -d /tmp/sam-installation && \
    /tmp/sam-installation/install && \
    rm -rf /tmp/aws-sam-cli.zip /tmp/sam-installation && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uv

# Copy requirements file first to leverage Docker cache
COPY pyproject.toml ./
COPY src/ ./src/

# uvをインストールする代わりに、標準のpipを使用
RUN pip install -e .

# Copy the rest of the application
COPY . .

CMD ["bash"]

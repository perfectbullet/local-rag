FROM jonfairbanks/local-rag

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

# Create and switch to a new user
WORKDIR /home/appuser
USER root

# Install application into container
COPY . .

# Install pipenv and compilation dependencies
RUN python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade pip
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN pip install -r requirements.txt
RUN pip install -e ./deal_excel_and_json

# Expose the Streamlit port
EXPOSE 8501 8502 8889 8888

# Setup a health check against Streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["python", "-m", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

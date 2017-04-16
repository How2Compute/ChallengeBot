#Get python
FROM python:3

# Copy source to app directory
COPY Source /pyBot
# Copy over the requirements file
COPY requirements.txt /pyBot/requirements.txt

# Set the default directory for the environment
ENV HOME /pyBot
WORKDIR /pyBot

# Install bots requirements
RUN pip install -r requirements.txt

# Set the run command
CMD [ "python", "./main.py" ]

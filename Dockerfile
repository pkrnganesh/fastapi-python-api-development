FROM python:3.9.7

WORKDIR /usr/src/app


# if we change any thing requirements.txt then you needed to rerun from this line

COPY requirements.txt ./ 

# here when we change any source code then it will only run this line of code just copying previous requirements since no changes in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .     

# while building image in docker using this code each line acts as a layer
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 


# from this file you will build an image using this you can create a container using command docker build -t fastapi . (. represents current directory)(fastapi is image name that i gave to it)


# we can build container using commands in cl command line by specifying the image names but what we do is add a docker compose file which consists all the commands so that we can just do docker compose up and down to build those containers
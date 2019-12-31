FROM ubuntu
RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 \
                        python3-dev \
                        python3-pip \
                        python3-tk \
                        build-essential \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
ENV HOME=/app
WORKDIR /app

RUN pip3 install numpy cython -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python3 ./dtaidistance/setup.py build_ext --inplace
RUN python3 ./dtaidistance/setup.py install
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENV FLASK_APP=./src/server.py

EXPOSE 8080

CMD python3 ./src/server.py
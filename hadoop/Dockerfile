FROM eclipse-temurin:8-jdk-jammy AS hadoop-files

COPY hadoop-3.3.6.tar.gz /tmp/hadoop.tar.gz

RUN mkdir -p /out \
    && tar -xzf /tmp/hadoop.tar.gz --strip-components=1 -C /out \
    && rm /tmp/hadoop.tar.gz

FROM eclipse-temurin:8-jdk-jammy

RUN apt-get update && apt-get install -y \
    openssh-server rsync procps net-tools wget curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash hduser

ENV JAVA_HOME=/opt/java/openjdk
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
ENV HADOOP_LOG_DIR=/home/hduser/hadoop-logs
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

COPY --from=hadoop-files /out /usr/local/hadoop
COPY config/ /usr/local/hadoop/etc/hadoop/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && mkdir -p /home/hduser/hdata /home/hduser/hadoop-logs \
    && chown -R hduser:hduser /home/hduser /usr/local/hadoop

USER hduser
WORKDIR /home/hduser

ENTRYPOINT ["/entrypoint.sh"]

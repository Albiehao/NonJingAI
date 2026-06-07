# 开发环境镜像 - 支持热重载
FROM maven:3.9-eclipse-temurin-17

WORKDIR /build

# 设置时区
ENV TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y --no-install-recommends tzdata curl && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# 复制 pom.xml
COPY pom.xml .

# 暴露端口
EXPOSE 8080

# 开发模式：使用 spring-boot:run 支持热重载
CMD ["mvn", "spring-boot:run", "-Dspring-boot.run.jvmArguments=-Dfile.encoding=UTF-8"]
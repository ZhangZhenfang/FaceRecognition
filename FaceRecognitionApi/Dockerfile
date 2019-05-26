FROM java:8

VOLUME /tmp

COPY target/facerecognition-0.0.1-SNAPSHOT.jar app.jar

RUN bash -c "touch /app.jar"

EXPOSE 8082

ENTRYPOINT ["java", "-jar", "app.jar", "--spring.profiles.active=test"]

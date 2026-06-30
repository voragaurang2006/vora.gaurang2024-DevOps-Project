# Multi-stage build Dockerfile
# Stage 1: Build the Maven application
FROM maven:3.8.4-openjdk-8-slim AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Create execution container
FROM openjdk:8-jre-slim
WORKDIR /app
COPY --from=build /app/target/corporate-website-1.0.0.jar app.jar
EXPOSE 8080

# Environment variables for health telemetry config
ENV SPRING_PROFILES_ACTIVE=prod

# Run the Spring Boot application
ENTRYPOINT ["java", "-jar", "app.jar"]

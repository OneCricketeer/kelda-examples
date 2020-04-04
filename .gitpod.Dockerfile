FROM cricketeerone/docker-kelda:0.1.0
VOLUME /app

USER root
RUN touch /workspace.yaml && chown gitpod:gitpod /workspace.yaml

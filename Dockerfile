FROM public.ecr.aws/docker/library/debian:bullseye-slim AS base

ARG USERNAME=vscode
ARG USER_UID=1000

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    \
    && curl -LSfs https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared \
    && chmod +x /usr/local/bin/cloudflared \
    \
    && groupadd -g ${USER_UID} ${USERNAME} \
    && useradd -u ${USER_UID} -g ${USER_UID} -m ${USERNAME} -s /bin/bash \
    && mkdir -p /etc/sudoers.d/ \
    && printf "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod -R 0440 /etc/sudoers.d/

FROM base

COPY ./requirements.txt /requirements.txt

USER ${USERNAME}

RUN python3 -m venv /home/${USERNAME}/Envs/miniproj/ \
    && . /home/${USERNAME}/Envs/miniproj/bin/activate \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && python3 -m pip install -r /requirements.txt \
    && mkdir -p /home/${USERNAME}/.vscode-server/extensions/ \
    && printf "\n. /home/${USERNAME}/Envs/miniproj/bin/activate\n" >> /home/${USERNAME}/.bashrc

WORKDIR /home/${USERNAME}/miniproj/

EXPOSE 8000 8001

ENTRYPOINT [ "./entrypoint.sh" ]

# kubectl helm rke yq
FROM alpine:3 as tools
RUN apk add --no-cache curl gzip
RUN curl -L --silent https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl -o /bin/kubectl
RUN curl -L --silent https://get.helm.sh/helm-v3.8.1-linux-amd64.tar.gz | zcat | tar xvf - linux-amd64/helm && mv linux-amd64/helm /bin/helm
RUN curl -L --silent https://github.com/rancher/rke/releases/download/v1.2.18/rke_linux-amd64 -o /bin/rke
RUN chmod +x /bin/kubectl /bin/helm /bin/rke

FROM python:alpine3.15 as ansible-modules
# Set PATH env var.
# Install building dependencies.
RUN apk add --no-cache build-base musl-dev libc-dev libffi-dev
# Import requirements file
COPY ./resources/ansible.requirements.yml /root/ansible.requirements.yml
COPY ./resources/python.requirements.yml /root/python.requirements.yml
# Activate the virtual env
RUN python -m venv /bin/venv
# Install the Ansible modules and their dependencies.
ENV PATH="/bin/venv/bin:$PATH"
RUN pip3 install -r /root/python.requirements.yml
RUN ansible-galaxy collection install -p /root/ansible_collections -r /root/ansible.requirements.yml

FROM python:alpine3.15 as finale
ENV PATH="/bin/venv/bin:$PATH"
RUN mkdir /data
RUN apk add --no-cache bash sudo
# from the host filesystem
COPY ./scripts/entrypoint.sh /root/entrypoint.sh
ADD ./ansible /root/.ansible
# from the `ansible-modules` layer
COPY --from=ansible-modules /bin/venv /bin/venv
COPY --from=ansible-modules /root/ansible_collections /root/.ansible/collections/ansible_collections
# from the `tools` layer
COPY --from=tools /bin/helm /bin/helm
COPY --from=tools /bin/rke /bin/rke
COPY --from=tools /bin/kubectl /bin/kubectl

# Set the entrypoint
ENTRYPOINT ["/root/entrypoint.sh"]

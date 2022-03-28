# [RKX](https://github.com/dontdoxxmeplz/rkx)
Another opinionated Kubernetes installer.

## Description

This image install Kubernetes RKE on specified nodes in the `config.yml` which is passed to the image through the `docker run` command arguments in a <ins>***Base64***</ins> format.

***Note.***

If the installation is successfull and you didnt mount the `/root/data` directory, the resulting kubeconfig file will be printed in the terminal console.

---

## Documentation

***Getting started***

```bash
$ docker pull --name rkx reallyseriousbus1ness0/rkx:[tag]
```

***Output***

If the installation is successfull and you didnt mount the `/root/data` directory, the resulting kubeconfig file will be printed in the terminal console.

***Configuration***

<ins>config.yml</ins>

```yaml
---
cluster:
  domain: example.com
  environment: dev
  user: 'admin'
  password: 'admin'
  ingress_controller: 'nginx'
  etcd_snapshots: True
  nodes:
    - address: 10.0.0.57
      hostname: 'cluster'
```

---

## Usage

***Examples***

**Install a standard Kubernetes RKE.**

```bash
$ docker run -it reallyseriousbus1ness0/rkx:[tag] lab "$(cat config.yml|base64 -w 0)"
```

**Uninstall Kubernetes RKE from the nodes.**

```bash
$ docker run -it reallyseriousbus1ness0/rkx:[tag] remove "$(cat config.yml|base64 -w 0)"
```

---
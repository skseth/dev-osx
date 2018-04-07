#!/usr/bin/env bash

docker pull registry:2 | grep -e 'Pulling from' -e Digest -e Status -e Error

docker run -d \
  -p 5001:5000 \
  --restart=always \
  --name regproxy \
  -e "REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io" \
  registry:2

sudo tee "/etc/docker/daemon.json" > /dev/null <<'EOF'
{
  "registry-mirrors": ["https://regproxy.local.test"]
}
EOF

systemctl restart docker

docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  registry:2

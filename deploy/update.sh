#!/bin/sh
set -eu
cd /opt/interior-design
git pull --ff-only origin main
UV_PYTHON_INSTALL_DIR=/opt/python /usr/local/bin/uv sync --frozen --no-dev --python 3.12
/usr/bin/caddy validate --config /opt/interior-design/Caddyfile --adapter caddyfile
install -m 644 deploy/interior-design.service /etc/systemd/system/interior-design.service
install -m 644 deploy/caddy.service /etc/systemd/system/caddy.service
install -m 644 Caddyfile /etc/caddy/Caddyfile
systemctl daemon-reload
systemctl restart interior-design
systemctl reload caddy
/usr/local/bin/uv cache clean

#!/bin/sh
set -eu
cd /opt/interior-design
git pull --ff-only origin main
UV_PYTHON_INSTALL_DIR=/opt/python /usr/local/bin/uv sync --frozen --no-dev --python 3.12
install -m 644 deploy/interior-design.service /etc/systemd/system/interior-design.service
install -m 644 deploy/nginx.conf /etc/nginx/sites-available/interior-design
nginx -t
systemctl daemon-reload
systemctl restart interior-design
systemctl reload nginx

# Развёртывание

Сервер: `ssh design-cite`, сайт: https://sadalskaya.ru.

Код передаётся через отдельный bare Git-репозиторий `/opt/interior-design.git`.
Рабочая копия: `/opt/interior-design`. Python 3.12 и зависимости устанавливает uv
по `uv.lock`. Caddy раздаёт `public/` и проксирует `/api/` на systemd-сервис.

Обновление после коммита (из локального проекта):

```sh
git push ssh://design-cite/opt/interior-design.git HEAD:main
ssh design-cite 'sh /opt/interior-design/deploy/update.sh'
```

Секреты находятся отдельно в `/etc/interior-design.env` (root, права 600).
В Git они не передаются.

Диагностика:

```sh
ssh design-cite 'systemctl status interior-design caddy --no-pager'
ssh design-cite 'journalctl -u interior-design -n 50 --no-pager'
```

Единственный исходный конфиг Caddy находится в `Caddyfile` в корне проекта.
При обновлении он проверяется, копируется в `/etc/caddy/Caddyfile` и применяется
мягкой перезагрузкой. Caddy сам выпускает и продлевает HTTPS-сертификаты.

На сервере адрес Telegram API из DNS (`149.154.166.110`) не отвечал.
В `/etc/hosts` задан доступный официальный адрес `149.154.167.220 api.telegram.org`;
HTTPS по-прежнему проверяет сертификат `api.telegram.org`. При будущих проблемах
с доставкой проверьте доступность этого адреса и актуальный DNS.

Caddy установлен официальным Linux-бинарником в `/usr/bin/caddy` (v2.11.4),
без Docker и Node.js. Сервис заявок использует один процесс Uvicorn.

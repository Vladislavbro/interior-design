# Развёртывание

Сервер: `ssh design-cite`, сайт: http://45.132.18.135.

Код передаётся через отдельный bare Git-репозиторий `/opt/interior-design.git`.
Рабочая копия: `/opt/interior-design`. Python 3.12 и зависимости устанавливает uv
по `uv.lock`. Nginx раздаёт `public/` и проксирует `/api/` на systemd-сервис.

Обновление после коммита (из локального проекта):

```sh
git push ssh://design-cite/opt/interior-design.git HEAD:main
ssh design-cite 'sh /opt/interior-design/deploy/update.sh'
```

Секреты находятся отдельно в `/etc/interior-design.env` (root, права 600).
В Git они не передаются.

Диагностика:

```sh
ssh design-cite 'systemctl status interior-design nginx --no-pager'
ssh design-cite 'journalctl -u interior-design -n 50 --no-pager'
```

Конфигурация пока для HTTP по IP. После подключения домена необходимо
настроить имя сервера и HTTPS, а также обновить deploy/nginx.conf.

Если хотите меня поддержать донатом) - https://www.donationalerts.com/r/aanxi3tyy

---------------------

Список IP которые стали недоступны 10.06.2025-xx.xx.2026, среди них - Amazon CDN, Amazon Cloudfront, Cloudflare, BunnyCDN, OVH SAS и прочие.

Все они брались с - https://stat.ripe.net/

--------------------

Пожалуйста, делайте pull requests сюда, дабы пополнить пул CIDR в данном листе, т.к нам необходимо восстановить работу интернета в России. Да поможет вам бог!

--------------

Если у вас не прогружаются сайты, выдает ошибку ERR_SSL_PROTOCOL_ERROR - поменяйте стратегию обхода с md5sig на badseq

---------

AS Parser - автоматически отыщет CIDR Адреса, отсортирует их в читабельный вид, и впринципе хороший скрипт. Поможет вам если вы хотите делать свой список + предлагать pull requests).

---------

Разблокировка Telegram если вы живете на юге России - Невозможна, используйте SOCKS5 или MTProto прокси. Блокировка реализована без использования ТСПУ провайдерами. Наглухо заблокирован только IP адрес веб морды (telegram.org). Зеркала для (telegram.org) как и адреса всех дата-центров заблокированы по портам (80 443 88 8443). Если нужно разблокировать и клиенты и вебсайты, то здесь только использование VPN. К сожалению zapret тут не поможет

---------

Список основан из репозитория **zapret** от Flowseal - https://github.com/Flowseal/zapret-discord-youtube

---------

Помогите поддержать проект звездочкой, поставьте ⭐ на этот репозиторий!

<a href="https://www.star-history.com/#V3nilla/IPSets-For-Bypass-in-Russia&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=V3nilla/IPSets-For-Bypass-in-Russia&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=V3nilla/IPSets-For-Bypass-in-Russia&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=V3nilla/IPSets-For-Bypass-in-Russia&type=date&legend=top-left" />
 </picture>
</a>

---

## Stage 1 модернизации (MVP foundation)

В репозитории добавлен первый этап поэтапной модернизации без массовой миграции данных.

### Что изменено
- Legacy-файлы в корне (`ipset-all.txt`, `exclude.txt`, `exclude-domains.txt`) пока остаются source input.
- Добавлен минимальный Python pipeline:
  - `python -m scripts.validate`
  - `python -m scripts.build`
- Добавлены базовые папки архитектуры: `scripts/`, `tests/`, `schemas/`, `sources/`, `dist/`, `build/`.

### Как запускать
```bash
python -m scripts.validate
python -m scripts.build
```

### Что генерируется
- `dist/ipset/ipset-all.txt`
- `dist/ipset/exclude.txt`
- `dist/ipset/exclude-domains.txt`
- `dist/manifest.json`

> Эти файлы generated и не предназначены для ручного редактирования.

### Важно
Это только первый этап миграции: добавлен фундамент архитектуры и MVP-нормализация/валидация, без полного рефакторинга и без генерации тяжёлых артефактов.

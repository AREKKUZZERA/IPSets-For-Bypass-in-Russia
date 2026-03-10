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

## Stage 2 модернизации (partial migration + stricter normalization)

Это второй этап после foundation/MVP: добавлена строгая внутренняя модель записей и частичная миграция в `sources/*.json`, без тяжёлых экспортов и release automation.

### Что нового
- Расширенная модель записи с полями метаданных и управлением `action`/`needs_review`.
- Частичная machine-readable миграция в `sources/stage2_seed.json`.
- Hybrid загрузка: одновременно новый `sources/*` и legacy-текстовые входы.
- Усиленная нормализация и валидация:
  - overlap detection;
  - include/exclude conflict detection;
  - IPv6 support;
  - фильтрация special-purpose диапазонов с переносом в `needs_review`.
- Улучшенный `dist/manifest.json`:
  - counts + stats by type/source;
  - warnings/problems;
  - needs_review section.
- CLI расширения:
  - `python -m scripts.validate [--strict] [--input-mode=legacy|hybrid|sources]`
  - `python -m scripts.build [--strict] [--input-mode=legacy|hybrid|sources]`

### Generated outputs
- `dist/ipset/ipset-all.txt`
- `dist/ipset/exclude.txt`
- `dist/ipset/exclude-domains.txt`
- `dist/manifest.json`

> Эти файлы generated и не предназначены для ручного редактирования.

### Ограничения текущего шага
- Не добавляются export-форматы sing-box/mihomo/nftables/.srs.
- Не добавляется release automation/scheduled update.
- Полная миграция legacy-датасета отложена на следующий этап.


---

## Stage 3 модернизации (export layer + modern text formats)

Добавлен модульный export layer, который генерирует legacy и современные форматы из единой нормализованной модели.

### Что нового
- Export architecture: `scripts/exporters/` + отдельные модули по форматам.
- Legacy ipset теперь проходит через новый exporter (compatibility target сохранён).
- Новые generated outputs:
  - sing-box source rule-set JSON (aggregate + split);
  - mihomo rule-providers (`yaml` + `text`);
  - nftables include sets (`ipv4`/`ipv6`).
- Профили сборки: `full`, `lite`, `domains-only`, `ip-only`.
- Manifest расширен артефактами export-слоя и предупреждениями по пустым экспортам.

### CLI
- `python -m scripts.build [--input-mode=legacy|hybrid|sources] [--profile=full|lite|domains-only|ip-only] [--strict]`

### Ограничения Stage 3
- `.srs` compile не включён (отложено).
- Нет release automation/scheduled update в этом шаге.

---

## Stage 4 модернизации (CI/CD + release readiness)

### Локальная сборка
- `make test`
- `make validate`
- `make build` (детерминированная сборка + checksums)
- `make deterministic-check` (двойная сборка и сравнение `dist/`)

### CI/CD overview
- `.github/workflows/validate.yml`:
  - unit tests;
  - validate прогон;
  - deterministic build smoke check.
- `.github/workflows/build.yml`:
  - сборка `dist/*`;
  - публикация artifacts workflow run.
- `.github/workflows/release.yml`:
  - запуск по semver-like tag `v*.*.*`;
  - валидация тега;
  - сборка deterministic `dist/*`;
  - публикация релиза с артефактами `dist/**`.
- `.github/workflows/scheduled-update.yml`:
  - cron-пересборка;
  - создание PR с изменениями через `create-pull-request`;
  - без прямого push в `main`.

### Release process
1. Подготовить изменения и убедиться, что `make deterministic-check` проходит.
2. Обновить `CHANGELOG.md`.
3. Создать и запушить тег `vMAJOR.MINOR.PATCH`.
4. Release workflow прикрепит `dist/*`, manifest и checksum-файлы.

### Scheduled update strategy
- Автообновление запускается по cron и вручную.
- Если есть diff в generated outputs, создаётся PR `chore/scheduled-update`.
- Maintainer review обязателен перед merge.

### Optional parts
- `.srs` compile остаётся optional и не является blocking-этапом CI/release.

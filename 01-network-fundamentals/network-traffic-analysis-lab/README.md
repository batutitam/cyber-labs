# Network Traffic Analysis Lab

## 1. Цель лабораторной

Изучить принципы захвата и анализа сетевого трафика с помощью **TShark**. На практике исследовать DNS-запросы, TCP-соединения и HTTP-обмен между клиентом и локальным сервером.

Лабораторная работа выполнена в собственной учебной среде на Ubuntu (WSL2).

## 2. Используемые инструменты

- **Ubuntu (WSL2)** — операционная среда.
- **TShark** — инструмент для захвата и анализа сетевых пакетов.
- **curl** — отправка HTTP-запросов.
- **Python HTTP Server** — локальный HTTP-сервер.
- **PCAP** — формат сохранения захваченного сетевого трафика.

## 3. Тестовая среда

Для анализа HTTP-трафика использовался локальный сервер:

- IP address: `127.0.0.1`
- Port: `8000`
- Network interface: `lo`

Для DNS-захвата использовался интерфейс `any`.

Все эксперименты проводились в локальной учебной среде.

## 4. DNS Traffic Analysis

### Захват DNS-трафика

Для захвата DNS-пакетов использовалась команда:

```bash
tshark -i any -f "port 53" -a duration:30
```

Во время захвата был выполнен DNS lookup:

```bash
getent ahostsv4 www.iana.org
```

В результате были обнаружены DNS Query и DNS Response.

### Наблюдаемые параметры

- DNS Query Name: `www.iana.org`
- Query Type: `A`
- DNS Transaction ID: `0xf430` (в одном из захватов)
- UDP Destination Port: `53`
- DNS Response: `No error`
- Answer: `198.18.2.203`
- TTL: `5 seconds`

Адрес `198.18.2.203` относится к диапазону `198.18.0.0/15`, зарезервированному для benchmarking. Поэтому его нельзя автоматически интерпретировать как обычный публичный IP-адрес сайта.

Также было замечено, что Source IP и Destination IP DNS-пакетов совпадали (`10.255.255.254`). Это наблюдение за DNS-трафиком в конкретной среде WSL2, а не универсальное поведение DNS.

### Анализ DNS-полей

Для отображения отдельных полей использовалась команда:

```bash
tshark -i any -f "port 53" -a duration:30 \
-T fields \
-e frame.number \
-e ip.src \
-e ip.dst \
-e udp.srcport \
-e udp.dstport \
-e dns.id \
-e dns.flags.response \
-e dns.qry.name \
-e dns.qry.type \
-e dns.a
```

Были изучены:

- Source IP и Destination IP;
- UDP Source Port и Destination Port;
- DNS Transaction ID;
- DNS Query Name;
- DNS Query Type;
- DNS Response и Answer.

## 5. TCP Traffic Analysis

Для исследования TCP-соединения использовался локальный HTTP-сервер на порту `8000`.

Запуск сервера:

```bash
python3 server.py
```

Захват трафика:

```bash
tshark -i lo -f "tcp port 8000" -a duration:20
```

HTTP-запрос отправлялся с помощью:

```bash
curl -v http://127.0.0.1:8000/
```

### TCP Three-Way Handshake

В захвате были обнаружены три начальных пакета:

1. `SYN` — клиент инициирует TCP-соединение.
2. `SYN, ACK` — сервер подтверждает запрос и отвечает.
3. `ACK` — клиент подтверждает ответ сервера.

Таким образом, был зафиксирован TCP Three-Way Handshake.

## 6. HTTP Traffic Analysis

После установления TCP-соединения клиент отправил:

```http
GET / HTTP/1.1
```

Локальный сервер ответил:

```http
HTTP/1.0 200 OK
```

В ответе также присутствовал Content-Type:

```http
Content-Type: text/plain
```

Для отображения HTTP-пакетов применялся Display Filter:

```bash
tshark -r ~/cyber-labs/http-traffic.pcap -Y "http"
```

В результате были обнаружены HTTP GET Request и HTTP 200 OK Response.

## 7. Capture Filters и Display Filters

В лабораторной работе были изучены два типа фильтрации.

**Capture Filter (`-f`)**

Применяется непосредственно во время захвата пакетов.

Пример:

```bash
tshark -i lo -f "tcp port 8000"
```

**Display Filter (`-Y`)**

Применяется для фильтрации пакетов при анализе захваченного трафика.

Пример:

```bash
tshark -r ~/cyber-labs/http-traffic.pcap -Y "tcp.flags.syn == 1"
```

Также проверялись фильтры:

```bash
-Y "http"
-Y "tcp.flags.fin == 1"
```

С помощью `tcp.flags.fin == 1` были обнаружены два пакета с FIN-флагом. Дополнительный анализ показал, что первый из них также декодируется как HTTP Response.

## 8. PCAP Analysis

Захват HTTP-трафика был сохранён в PCAP:

```bash
tshark -i lo -f "tcp port 8000" \
-a duration:20 \
-w ~/cyber-labs/http-traffic.pcap
```

Для повторного анализа использовалась команда:

```bash
tshark -r ~/cyber-labs/http-traffic.pcap
```

Для отображения TCP Conversations:

```bash
tshark -r ~/cyber-labs/http-traffic.pcap -q -z conv,tcp
```

### Результаты TCP Conversation

- Client: `127.0.0.1:47388`
- Server: `127.0.0.1:8000`
- Total Frames: `12`
- Total Bytes: `1042`
- Observed Duration: approximately `0.0012 seconds`

В захвате были обнаружены TCP Handshake, HTTP Request, HTTP Response и последовательность завершения TCP-соединения.

## 9. Основные результаты

В ходе лабораторной работы удалось:

- Выполнить захват DNS-трафика.
- Разобрать структуру DNS Query и DNS Response.
- Изучить Source IP, Destination IP и Port Numbers.
- Обнаружить TCP Three-Way Handshake.
- Проанализировать HTTP GET Request и HTTP 200 OK Response.
- Применить Capture Filters и Display Filters.
- Исследовать TCP Flags, включая SYN, ACK и FIN.
- Сохранить сетевой трафик в PCAP.
- Повторно открыть PCAP и проанализировать TCP Conversations.

## 10. Вывод

В ходе лабораторной работы были получены практические навыки захвата и анализа сетевого трафика с помощью TShark.

Были изучены основные этапы установления и завершения TCP-соединения, структура DNS-запросов и ответов, а также обмен HTTP-данными между клиентом и локальным сервером.

Полученные навыки являются основой для дальнейшего изучения Network Traffic Analysis, Blue Team Operations и SOC Investigation.

---

**Project Type:** Educational Lab  
**Environment:** Local Ubuntu (WSL2)  
**Scope:** Authorized local testing only

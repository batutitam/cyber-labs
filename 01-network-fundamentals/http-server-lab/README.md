# HTTP Server Lab

## Overview

This is an educational cybersecurity lab focused on HTTP fundamentals and basic HTTP server implementation using Python.

The project demonstrates how an HTTP server handles GET and POST requests, reads request headers, processes request bodies, and responds with appropriate HTTP status codes.

## Technologies

- Python 3
- `http.server`
- `HTTPServer`
- `BaseHTTPRequestHandler`
- cURL
- HTTP/1.0 and HTTP/1.1 fundamentals

## Features

- Handles HTTP GET requests.
- Handles HTTP POST requests.
- Reads and displays incoming HTTP headers.
- Processes JSON request bodies.
- Accepts `application/x-www-form-urlencoded` data.
- Detects invalid JSON using exception handling.
- Returns HTTP 400 Bad Request for invalid JSON.
- Returns HTTP 200 OK for successfully processed requests.

## Project Structure

```text
http-server-lab/
├── server.py
└── README.md
```

## How to Run

Start the server:

```bash
python3 server.py
```

The server listens on:

```text
http://127.0.0.1:8000
```

## Testing

### 1. Valid JSON POST request

```bash
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"alex","role":"analyst"}' \
  http://127.0.0.1:8000/
```

Expected result: `HTTP 200 OK`.

### 2. Invalid JSON POST request

```bash
curl -i -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"alex","role":"analyst"' \
  http://127.0.0.1:8000/
```

Expected result: `HTTP 400 Bad Request`.

### 3. Form URL Encoded POST request

```bash
curl -i -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&role=analyst" \
  http://127.0.0.1:8000/
```

Expected result: `HTTP 200 OK`.

## Key Learning Outcomes

- Understanding HTTP request and response structure.
- Identifying HTTP methods and status codes.
- Understanding the purpose of Content-Type and Content-Length.
- Processing JSON data in Python.
- Handling malformed input with exceptions.
- Using cURL to test HTTP endpoints.

## Security Notes

This is a local educational project, not a production-ready web server.

The server is bound to `127.0.0.1` and is intended for local testing only.

## Project Type

Educational cybersecurity lab — HTTP Fundamentals.

# Top K IPs with ERROR Logs

## Description

Given a log file where each line starts with an IP address and includes a log level token, print the top `k` IP addresses that generated `ERROR` logs.

## Input

- path to `app.log`
- integer `k`

## Output

One line per result:

```text
<ip> <count>
```

sorted by descending count and then lexicographically by IP.

## Hints

- Start with `grep " ERROR "`.
- Extract IP with `awk '{print $1}'`.
- Aggregate with `sort | uniq -c`.
- Finish sorting and trim with `head`.

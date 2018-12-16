VodafoneBeGone
==============

This repo contains a prometheus exporter which gets your current isp connection speed via [fast.com][1] and [speedtest.net][3]

According to this [article][2] your German ISP contract can be canceled via `Sonderkündigung` if your internet Speed is lower than `90%` of the promissed speed on 20 random messurements *via Cable* 

# Setup 
Install a [Raspberry pi][4] or similar on your cable box and run this project
``` python app.py start --service isp -u localhost -p 9999```
## Prometheus
Configure your Prometheus instance to pick up the metrics.
```
scrape_configs:
  - job_name: isp
    scrape_interval: 14400s
    scrape_timeout: 120s
    static_configs:
    - targets: ['$IP_OF_YOUR_DEVICE:9999']
```
For test purposes i recommend the following [docker-compose][6] stack

## Grafana
The `grafana_isp_dashboard.json` can be imported via web console

# Feedback
i try to collect metrics to get rid of my shitty Vodafone Contract and i'll post updates if it works.
Let me know how it goes for you.

# Special thanks
[sanderjo][5] for the fast.com library


[1]: fast.com
[2]: https://www.google.com/search?client=ubuntu&channel=fs&q=internet+zu+langsam+sonderk%C3%BCndigung&ie=utf-8&oe=utf-8
[3]: speedtest.net
[4]: https://amzn.to/2zV9VQj
[5]: https://github.com/sanderjo/fast.com
[6]: https://github.com/vegasbrianc/prometheus
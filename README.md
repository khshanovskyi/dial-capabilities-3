<h1 align="center">
         DIAL Platform Capabilities Presentation: Part 3
    </h1>
    <p align="center">
        <p align="center">
        <a href="https://dialx.ai/">
          <img src="https://dialx.ai/dialx_logo.svg" alt="About DIALX">
        </a>
    </p>
<h4 align="center">
    <a href="https://discord.gg/ukzj9U9tEe">
        <img src="https://img.shields.io/static/v1?label=DIALX%20Community%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
</h4>

Here we will configure [DIAL Admin](https://docs.dialx.ai/tutorials/admin/home) application to configure models, applications and other stuff + analytics.

![DIAL Admin](/screenshots/services.png)

- [1. Run DIAL Admin with Analytics](#1-run-dial-admin-with-analytics)
- [2. ](#2-)
- [3. ](#3-)
- [4. ](#4)

---

## 1. Run DIAL Admin with Analytics

**Run [docker-compose.yml](docker-compose.yml)**
It will start such services:
- Keycloak, it will be our auth provider, the configuration with `realm` in [/keycloak/import/realm-config.json](/keycloak/import/realm-config.json)
- Redis + Core (core is the heart of DIAL platform), Adapters to works with different vendors, and Themes + Chat
- Influxdb, here we will store all the logs and analytics
- Vector (in compose it is `logger` service): reads logs from DIAL Core logs and send them to Analytics Realtime
- [Analytics](https://github.com/epam/ai-dial-analytics-realtime) to process logs from Vector, create topics and snd all of that to Influxdb
- Admin Backend+Frontend to work with DIAL Core configuration and show realtime analytics
- Prometheus and Grafana to read the logs (these services are optional)

---

## 2. 


---

## 3. 


---
## 4.


---
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

Here we will set up [DIAL Admin](https://docs.dialx.ai/tutorials/admin/home) application to configure models,
applications and other stuff + analytics.

![---](/screenshots/services.png)

- [1. Run DIAL Admin with Analytics](#1-run-dial-admin-with-analytics)
- [2. Add first LLM through DIAL Admin](#2-add-first-llm-through-dial-admin)
- [3. Add different models](#3-add-different-models)
- [4. Add Application](#4-add-application)
- [5. Check Analytics](#5-check-analytics)

---

## 1. Run DIAL Admin with Analytics

**Run [docker-compose.yml](docker-compose.yml)**
It will start such services:

- Keycloak, it will be our auth provider, the configuration with `realm`
  in [/keycloak/import/realm-config.json](/keycloak/import/realm-config.json)
- Redis + Core (core is the heart of DIAL platform), Adapters to works with different vendors, and Themes + Chat
- Influxdb, here we will store all the logs and analytics
- Vector (in compose it is `logger` service): reads logs from DIAL Core logs and send them to Analytics Realtime
- [Analytics](https://github.com/epam/ai-dial-analytics-realtime) to process logs from Vector, create topics and snd all
  of that to Influxdb
- Admin Backend+Frontend to work with DIAL Core configuration and show realtime analytics
- Prometheus and Grafana to read the logs (these services are optional)

---

## 2. Add first LLM through DIAL Admin

1. **Log in**:

    | URL                   | Description |
    |-----------------------|-------------|
    | http://localhost:3100 | DIAL Chat   |
    | http://localhost:3102 | DIAL Admin  |
    | http://localhost:8900 | Keycloak    |
    
    There are three default DIAL users pre-defined in Keycloak:
    
    | Username   | Password | Description                                |
    |------------|----------|--------------------------------------------|
    | user       | dial     | Has only basic access to **DIAL Chat**     |
    | dial       | dial     | Has admin access to **DIAL Chat**          |
    | dial-admin | dial     | Has access to **DIAL Admin** console       |
    
    To log in to **Keycloak** as administrator
    
    | Username   | Password |       
    |------------|----------|
    | admin      | admin    |  

2. Add OpenAI Adapter

    <details><summary>Instruction</summary>
    
    - Go to Builders > Adapters
     ![---](/screenshots/adapters.png)
    - Create OpenAI Adapter:
    
        | Parameter     | Value                                              |
        |---------------|----------------------------------------------------|
        | ID            | openai-adapter                                     |
        | Display name  | OpenAI Adapter                                     |
        | Base endpoint | http://adapter-dial-openai:5000/openai/deployments |
        ![---](/screenshots/adapters-openai-create.png)
        ![---](/screenshots/adapters-openai-created.png)
    
    </details>

3. Add OpenAI model

    <details><summary>Instruction</summary>
    
    - Go to Entities > Models
      ![---](/screenshots/models.png)
    
        | Parameter    | Value          |
        |--------------|----------------|
        | ID           | gpt-4o         |
        | Display name | GPT 4o         |
        | Adapter      | OpenAI Adapter |
        
        ![---](/screenshots/models-gpt4o-create.png)
        
        | Parameter         | Value                                      |
        |-------------------|--------------------------------------------|
        | Override name     | gpt-4o                                     |
        | Upstream endpoint | https://api.openai.com/v1/chat/completions |
        | Key               | ${YOUR_OPENAI_API_KEY}                     |
        | Tokens            | 2.5 && 10                                  |
        
        ![---](/screenshots/models-gpt4o-configure-1.png)
        ![---](/screenshots/models-gpt4o-configure-2.png)
        
        Disable roles for this model
        ![---](/screenshots/models-gpt4o-configure-3.png)
    
    </details>

4. Test it (**pay attention** that it could take some time to reload DIAL Core config after update)

    <details><summary>Sample</summary>
    
   Open http://localhost:3100/marketplace and login as `user` and test it 
      ![---](/screenshots/models-gpt4o-test.png)
      ![---](/screenshots/models-gpt4o-test-2.png)
           
    </details>

---

## 3. Add different models

### Anthropic Sonnet 4 LLM:

<details><summary>Instruction</summary>

1. Add `bedrock` adapter:

   | Parameter     | Value                                               |
   |---------------|-----------------------------------------------------|
   | ID            | bedrock-adapter                                     |
   | Display name  | Bedrock Adapter                                     |
   | Base endpoint | http://adapter-dial-bedrock:5000/openai/deployments |
   ![---](/screenshots/adapters-bedrock.png)
2. Add `claude-sonnet-4` model

   | Parameter    | Value                     |
   |--------------|---------------------------|
   | ID           | claude-sonnet-4           |
   | Display name | Claude Sonnet-4           |
   | Adapter      | Bedrock Adapter           |
   | Endpoint     | claude-sonnet-4-20250514  |
   | Key          | ${YOUR_ANTHROPIC_API_KEY} |
   | Tokens       | 3 && 15                   |
   ![---](/screenshots/models-sonnet-create.png)
   ![---](/screenshots/models-sonnet-configure-endpoint.png)
   ![---](/screenshots/models-sonnet-configure.png)

   Disable roles for this model
   ![---](/screenshots/models-sonnet-role.png)

3. Test it
   ![---](/screenshots/models-sonnet-marketplace.png)
   ![---](/screenshots/models-sonnet-test.png)

</details>

### OpenAI TTS:

<details><summary>Instruction</summary>

1. We already have OpenAI Adapter, so you can move to the 2nd point
2. Add `gpt-4o-mini-tts` model (don't forget to disable roles for this model)

   | Parameter         | Value                                   |
         |-------------------|-----------------------------------------|
   | ID                | gpt-4o-mini-tts                         |
   | Display name      | GPT 4o Mini TTS                         |
   | Adapter           | OpenAI Adapter                          |
   | Upstream endpoint | https://api.openai.com/v1/audio/speech  |
   | Key               | ${YOUR_OPENAI_API_KEY}                  |
   | Tokens            | 3                                       |

3. Test it
   ![---](/screenshots/models-tts-test-1.png)
   ![---](/screenshots/models-tts-test-2.png)

</details>

---

## 4. Add Application

<details><summary>Instruction</summary>

1. Run [essay_assistant](app_demo/d1_essay_assistant/essay_assistant.py).
2. Configure application

    | Parameter              | Value                                                                                    |
    |------------------------|------------------------------------------------------------------------------------------|
    | ID                     | essay-assistant-gpt                                                                      |
    | Display name           | Essay Assistant                                                                          |
    | Completion Endpoint    | http://host.docker.internal:5025/openai/deployments/essay-assistant-gpt/chat/completions |
    | Configuration Endpoint | http://host.docker.internal:5025/openai/deployments/essay-assistant-gpt/configuration    |
        
   ![---](/screenshots/app-marketplace.png)
   ![---](/screenshots/app-features.png)
   ![---](/screenshots/app-roles.png)
   ![---](/screenshots/app-test-1.png)
   ![---](/screenshots/app-test-2.png)

</details>

---

## 5. Check Analytics

- You can check global dashboard with deployments usage
  ![---](/screenshots/dashboard.png)
- Also, you can check such dashboard with usage and activities for specific model
  ![---](/screenshots/dashboard-gpt.png)
- You can check global activities on the platform
  ![---](/screenshots/activities.png)
- And usage logs
  ![---](/screenshots/usage-log.png)

---
# Webhooks

This document explains how to use webhooks in Mubble to receive updates from Telegram.

## Overview

Mubble supports two methods for receiving updates from Telegram:

1. **Long polling**: Continuously requesting updates from Telegram (default method)
2. **Webhooks**: Telegram sends updates to your server via HTTP requests

Webhooks are more efficient than long polling because:
- They reduce latency since updates are pushed to your server immediately
- They eliminate the need for continuous polling, reducing server load
- They work well with serverless architectures

However, webhooks require:
- A publicly accessible HTTPS server with a valid SSL certificate
- Proper server configuration to handle incoming webhook requests

## Setting Up Webhooks

### Basic Webhook Setup

To set up a webhook in Mubble, you need to:

1. Create a Mubble bot instance
2. Configure the webhook settings
3. Start the webhook server

Here's a basic example:

```python
from mubble import API, Mubble, Token, WebhookConfig
from mubble.server import WebhookServer

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Configure webhook
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    certificate=None,  # Path to certificate file if self-signed
    ip_address=None,  # Optional IP address
    max_connections=40,  # Maximum number of connections
    allowed_updates=["message", "callback_query"],  # Types of updates to receive
    drop_pending_updates=True,  # Whether to drop pending updates
    secret_token="your-secret-token"  # Secret token to validate webhook requests
)

# Create webhook server
server = WebhookServer(
    bot=bot,
    webhook_config=webhook_config,
    host="0.0.0.0",  # Server host
    port=8443,  # Server port
    path="/webhook"  # Webhook endpoint path
)

# Start the webhook server
if __name__ == "__main__":
    server.run()
```

### Using with AIOHTTP

Mubble's webhook server is built on AIOHTTP. You can integrate it with an existing AIOHTTP application:

```python
from aiohttp import web
from mubble import API, Mubble, Token, WebhookConfig
from mubble.server import setup_webhook

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Configure webhook
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    secret_token="your-secret-token"
)

# Create AIOHTTP application
app = web.Application()

# Add your routes
app.router.add_get("/", lambda request: web.Response(text="Bot is running"))

# Setup webhook
setup_webhook(
    app=app,
    bot=bot,
    webhook_config=webhook_config,
    path="/webhook"
)

# Start the application
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8443)
```

### Using with FastAPI

You can also integrate Mubble webhooks with FastAPI:

```python
import uvicorn
from fastapi import FastAPI, Request, Response
from mubble import API, Mubble, Token, WebhookConfig
from mubble.server import process_update

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Configure webhook
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    secret_token="your-secret-token"
)

# Set webhook
async def setup():
    await api.set_webhook(webhook_config)

# Create FastAPI application
app = FastAPI()

# Add webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    # Verify secret token
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != webhook_config.secret_token:
        return Response(status_code=403)
    
    # Process update
    update_data = await request.json()
    await process_update(bot, update_data)
    
    return Response(status_code=200)

# Add startup event
@app.on_event("startup")
async def on_startup():
    await setup()

# Add shutdown event
@app.on_event("shutdown")
async def on_shutdown():
    await api.delete_webhook(drop_pending_updates=True)

# Start the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8443)
```

## Webhook Security

### Secret Token

Always use a secret token to validate webhook requests:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    secret_token="your-secret-token"  # Use a strong, random token
)
```

Telegram will include this token in the `X-Telegram-Bot-Api-Secret-Token` header of webhook requests. You should verify this token to ensure the request is from Telegram.

### SSL Certificate

Telegram requires HTTPS for webhooks. You can:

1. Use a domain with a valid SSL certificate
2. Use a self-signed certificate (not recommended for production)

If using a self-signed certificate:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    certificate="/path/to/certificate.pem"  # Path to your certificate file
)
```

### IP Filtering

You can restrict webhook requests to Telegram's IP addresses:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    ip_address="149.154.167.220"  # One of Telegram's IP addresses
)
```

## Advanced Webhook Configuration

### Allowed Updates

Specify which types of updates you want to receive:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    allowed_updates=[
        "message",
        "edited_message",
        "callback_query",
        "inline_query"
    ]
)
```

This reduces unnecessary traffic and processing.

### Max Connections

Control the maximum number of simultaneous HTTPS connections:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    max_connections=100  # Default is 40
)
```

### Drop Pending Updates

Clear the update queue when setting up the webhook:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    drop_pending_updates=True
)
```

This is useful when restarting your bot to avoid processing old updates.

## Webhook vs. Long Polling

### When to Use Webhooks

Webhooks are ideal for:
- Production environments with stable servers
- Serverless architectures (AWS Lambda, Google Cloud Functions, etc.)
- High-traffic bots where efficiency is important
- Environments where you need immediate update processing

### When to Use Long Polling

Long polling is better for:
- Development and testing
- Environments without a public HTTPS server
- Simple bots with low traffic
- Environments where setting up webhooks is difficult

### Switching Between Methods

You can easily switch between webhooks and long polling:

```python
# Switch to webhooks
await api.set_webhook(webhook_config)

# Switch to long polling
await api.delete_webhook()
await bot.start_polling()
```

## Deployment Considerations

### Serverless Deployment

For AWS Lambda:

```python
from mubble import API, Mubble, Token, Update
import json

api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

async def lambda_handler(event, context):
    # Extract update data from the event
    body = json.loads(event["body"])
    
    # Process the update
    await bot.process_update(Update.model_validate(body))
    
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"})
    }
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8443

CMD ["python", "bot.py"]
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.pem;
    ssl_certificate_key /path/to/private.key;

    location /webhook {
        proxy_pass http://localhost:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Common Issues

1. **Webhook URL must be HTTPS**: Ensure your webhook URL uses HTTPS with a valid certificate.

2. **Connection refused**: Check that your server is running and accessible from the internet.

3. **Certificate verification failed**: Ensure your SSL certificate is valid and properly configured.

4. **Webhook request timeout**: Optimize your handler code to respond quickly (under 10 seconds).

5. **IP address not allowed**: If you specified an IP address, ensure it matches Telegram's servers.

### Debugging Webhooks

To check your webhook status:

```python
webhook_info = await api.get_webhook_info()
if webhook_info.is_ok():
    info = webhook_info.unwrap()
    print(f"URL: {info.url}")
    print(f"Pending updates: {info.pending_update_count}")
    print(f"Last error: {info.last_error_message}")
```

To test webhook locally, you can use tools like ngrok:

```bash
ngrok http 8443
```

Then use the generated HTTPS URL for your webhook.

## Best Practices

### Respond Quickly

Telegram expects your server to respond within 10 seconds. Keep your handlers efficient.

### Handle Errors Gracefully

Implement proper error handling to prevent your webhook from failing:

```python
@bot.on.message()
async def handler(message):
    try:
        # Your handler code
        await message.answer("Processing your request...")
        result = await process_request(message.text)
        await message.answer(f"Result: {result}")
    except Exception as e:
        # Log the error
        logger.error(f"Error in handler: {e}")
        # Provide a user-friendly response
        await message.answer("Sorry, an error occurred while processing your request.")
```

### Use Allowed Updates

Only request the update types your bot actually needs:

```python
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    allowed_updates=["message", "callback_query"]  # Only what you need
)
```

### Implement Health Checks

Add a health check endpoint to monitor your bot's status:

```python
@app.get("/health")
async def health_check():
    # Check if the bot is connected to Telegram
    me = await api.get_me()
    if me.is_ok():
        return {"status": "ok", "bot_name": me.unwrap().username}
    else:
        return {"status": "error", "message": "Cannot connect to Telegram API"}
```

## Next Steps

Now that you understand webhooks in Mubble, you can explore:

- [Middleware](middleware.md)
- [Error Handling](error-handling.md)
- [State Management](state-management.md)
- [Handlers](handlers.md) 
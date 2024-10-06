# TATNEFT risk tracker

A [TG bot]() for creating service tickets in IntraService.

## FEATURES

* Telegram WebApp calendar to select date of the encountered risk and fill the forms for ticket creation (in progress)
* Send service tickets to IntraService via API (in progress)
* Rating system for employees based on service tickets creation & resolution (in progress)
* Reports generation (in progress)

## DEPENDENCIES
- [aiogram](https://github.com/aio-libs/aiohttp)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [nginx](https://www.nginx.com/)
- [certbot](https://certbot.eff.org/)
- [uvicorn](https://www.uvicorn.org/)
- [celery](https://github.com/celery/celery)
- [redis](https://redis.io/)
- [fastapi](https://fastapi.tiangolo.com/)
- [postgresql](https://www.postgresql.org/)


## INSTALLATION
```bash
pip install -r requirements.txt
sudo apt install certbot nginx python3-certbot-nginx
```


## NGINX server configuration
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name yourdomain.com;  # Replace with your domain or IP address

    location / {
        proxy_pass http://127.0.0.1:8000;  # FastAPI app running on this port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90;
        proxy_connect_timeout 90;
    }

    # Optional: Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

# HTTPS server configuration
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90;
        proxy_connect_timeout 90;
    }
}
```

Obtain a SSL certificate from Let's Encrypt.
```bash
sudo certbot --nginx -d yourdomain.com
```

Automatically renew the SSL certificate.
```bash
sudo certbot renew --dry-run
```

Test the configuration.
```bash
sudo nginx -t
```

Restart the server.
```bash
sudo systemctl restart nginx
```


## RUNNING
Start FastAPI app.
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
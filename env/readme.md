To align the paths in the systemd unit file with your project's structure and update the Gunicorn and Nginx configurations accordingly, you can follow these steps:

### Step 1: Environment Preparation

Make sure you have Python 3.12 installed along with Pip, Gunicorn, and Nginx.

### Step 2: Project Structure

Assuming your project structure looks like this:

```
/home/username/Kitchen-Recipes-Tests/
├── kr-tests/
│   └── bin/
│       └── gunicorn
├── kr-tests.sock
├── wsgi.py
└── README.md
```

### Step 3: Update Gunicorn Configuration (systemd unit file)

Modify the systemd unit file (`kr-tests.service`) located at `/etc/systemd/system/` or `/lib/systemd/system/` to reflect your project's paths:

```ini
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=zperk
Group=www-data
WorkingDirectory=/home/username/Kitchen-Recipes-Tests
Environment="PATH=/home/username/Kitchen-Recipes-Tests/kr-tests/bin"
ExecStart=/home/username/Kitchen-Recipes-Tests/kr-tests/bin gunicorn --workers 3 --bind unix:/home/username/Kitchen-Recipes-Tests/kr-tests.sock -m 007 wsgi:WEBAPP
```

### Step 4: Update Nginx Configuration

Modify your Nginx configuration file (typically found in `/etc/nginx/sites-available/` or `/etc/nginx/conf.d/`) to pass requests to Gunicorn:

```nginx
server {
    listen 80;
    server_name [YOUR DOMAIN OR LOCAL IP]; # YOU MUST MODIFY THIS!

    location / {
        proxy_pass http://unix:/home/username/Kitchen-Recipes-Tests/kr-tests.sock; # Unix socket path
        include proxy_params;
    }
}
```

### Step 5: Enable the Changes

After making these changes, you need to reload systemd and Nginx to apply the configurations:

```bash
# Reload the engine(s).
sudo systemctl daemon-reload
sudo systemctl restart kr-tests
sudo systemctl restart nginx
# Start and check the engine(s).
sudo systemctl start kr-tests
sudo systemctl enable kr-tests
sudo systemctl status kr-tests
```

### Step 6: Testing

Navigate to your domain or IP to test your Flask application deployed on Gunicorn and Nginx.

With these modifications, your project's paths in the systemd unit file and Nginx configuration will be aligned with your project's structure.

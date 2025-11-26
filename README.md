# Coolify Volume Bug Demonstration

This repository demonstrates a bug in Coolify's preview deployment system where services sharing volumes end up with different base paths due to a UUID variable mutation in the compose parser.

## The Bug

When deploying a pull request with docker-compose, the second and subsequent services get an incorrect volume path with an extra PR ID suffix on the UUID portion.

**Expected behavior:** All services share the same base path:
```
/data/coolify/applications/abc123/static-pr-1
/data/coolify/applications/abc123/media-pr-1
```

**Actual behavior:** Services have different base paths:
```
nginx:  /data/coolify/applications/abc123/static-pr-1
web:    /data/coolify/applications/abc123-1/static-pr-1
```

This breaks volume sharing between services (e.g., nginx can't serve files written by the web service).

## Repository Structure

```
.
├── docker-compose.yml          # Main compose file with shared volumes
├── devops/
│   ├── nginx/
│   │   ├── Dockerfile         # Nginx container
│   │   └── nginx.conf         # Nginx configuration
│   └── web/
│       ├── Dockerfile         # Python Flask web app
│       ├── app.py             # Simple Flask app
│       └── entrypoint.sh      # Startup script
├── static/                    # Shared static files directory
└── media/                     # Shared media files directory
```

## How to Use This Repository

### 1. Deploy to Coolify

1. Fork or push this repository to your GitHub/GitLab
2. In Coolify, create a new Application
3. Select this repository
4. Choose "Docker Compose" as the build pack
5. **Important:** Configure a public domain for the `nginx` service (this triggers the bug)
6. Enable Preview Deployments

### 2. Create a Pull Request

```bash
git checkout -b test-pr
echo "test change" >> README.md
git commit -am "Test PR for bug reproduction"
git push origin test-pr
```

Create a PR from `test-pr` to `main`.

### 3. Verify the Bug

After Coolify deploys the preview, SSH into your Coolify server and check:

```bash
# View the generated compose file (replace with your app UUID and PR number)
cat /data/coolify/applications/<UUID>/docker-compose.yml

# Check actual volume mounts
docker inspect nginx-<UUID>-pr-1 | grep -A 20 Mounts
docker inspect web-<UUID>-pr-1 | grep -A 20 Mounts
```

You should see that `nginx` and `web` have different volume source paths.

### 4. Test Volume Sharing

If the volumes were working correctly, you could:

```bash
# Web service writes files
curl http://your-preview-domain.com/write-test

# Nginx should serve those files
curl http://your-preview-domain.com/static/test.txt
curl http://your-preview-domain.com/media/test.txt
```

With the bug, nginx returns 404 because it's looking in a different directory.

## Technical Details

The bug is in `bootstrap/helpers/parsers.php` in the `applicationParser()` function at lines 1210-1213:

```php
$uuid = $resource->uuid;
if ($isPullRequest) {
    $uuid = "{$resource->uuid}-{$pullRequestId}";  // Bug: mutates shared variable
}
```

This mutation affects all services processed after the first service with an FQDN.

## Related Issue

See: [Coolify Issue #XXXX](https://github.com/coollabsio/coolify/issues/XXXX)

## License

MIT - This is a bug demonstration repository, use freely.

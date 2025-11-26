# Testing the Volume Bug

This pull request is created to test and demonstrate the Coolify volume bug in preview deployments.

## What to Check After Deployment

1. **SSH into your Coolify server** and check the generated docker-compose file:
   ```bash
   cat /data/coolify/applications/<YOUR-APP-UUID>/docker-compose.yml
   ```

2. **Look for volume paths** in the nginx and web services. You should see:
   - **nginx-pr-X**: `/data/coolify/applications/<UUID>/static-pr-X`
   - **web-pr-X**: `/data/coolify/applications/<UUID>-X/static-pr-X` ❌ (BUG!)

   Notice the extra `-X` suffix in the web service's volume path.

3. **Inspect running containers**:
   ```bash
   docker inspect nginx-<UUID>-pr-X | grep -A 20 Mounts
   docker inspect web-<UUID>-pr-X | grep -A 20 Mounts
   ```

   The source paths will be different, preventing volume sharing.

4. **Test volume sharing** (this will fail due to the bug):
   ```bash
   # Web writes files
   curl http://your-preview-domain.com/write-test

   # Nginx should serve them (but won't due to different volume paths)
   curl http://your-preview-domain.com/static/test.txt  # 404 error
   ```

## Expected vs Actual

### Expected (correct behavior)
Both services use the same volume base path:
```
nginx: /data/coolify/applications/abc123/static-pr-1:/var/www/static:ro
web:   /data/coolify/applications/abc123/static-pr-1:/var/www/static
```

### Actual (buggy behavior)
Services have different base paths:
```
nginx: /data/coolify/applications/abc123/static-pr-1:/var/www/static:ro
web:   /data/coolify/applications/abc123-1/static-pr-1:/var/www/static
```

This breaks the volume sharing mechanism between nginx and web services.

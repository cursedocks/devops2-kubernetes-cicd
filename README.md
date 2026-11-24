## Environments

### Development
- Namespace: dev
- Replicas: 2
- Automatic deployment through GitHub Actions

### Production
- Namespace: prod
- Replicas: 3
- Separate Helm configuration
- Manual deployment and rollback

## Deployment

Deploy to development:

    helm upgrade --install fastapi ./helm -n dev -f helm/values-dev.yaml

Deploy to production:

    helm upgrade --install fastapi ./helm -n prod -f helm/values-prod.yaml

Rollback production:

    helm rollback fastapi 1 -n prod

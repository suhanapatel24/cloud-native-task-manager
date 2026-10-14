# Deployment Evidence

Do not claim a live Kubernetes deployment until these checks are completed.

- [ ] CI tests pass
- [ ] Docker image builds
- [ ] Docker Compose API and MySQL start successfully
- [ ] CRUD data persists through MySQL
- [ ] Kubernetes Secret created outside source control
- [ ] Kubernetes resources applied
- [ ] API replicas are Ready
- [ ] MySQL PVC is Bound
- [ ] LoadBalancer endpoint responds
- [ ] CRUD operation succeeds against deployed endpoint

Capture sanitized command output/screenshots here after verification. Never capture or commit secret values.

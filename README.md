# Daily Startup Guide - Minikube & ArgoCD

## 1. Start Minikube

```bash
cd ~/projetos/agri-curve
minikube start
```

Wait for message: "Done! kubectl is now configured to use 'minikube'"

Verify cluster is running:
```bash
kubectl get nodes
```

Should show minikube node in Ready status.

---

## 2. Start Volume Mount (CRITICAL)

**Open a dedicated terminal window and keep it running:**

```bash
cd ~/projetos/agri-curve
minikube mount $(pwd)/data/processed:/mnt/agri-data
```

**Important:** This terminal must stay open while working. Data saved by pipeline appears in `data/processed/` folder.

---

## 3. Verify ArgoCD is Running

```bash
kubectl get pods -n argocd
```

All pods should show `1/1 Running`. If not, wait 30-60 seconds for ArgoCD to start.

---

## 4. Access ArgoCD UI

**In a new terminal (keep mount terminal open):**

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Keep this terminal open. Access ArgoCD at: http://localhost:8080

**Get admin password:**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo
```

Login with:
- Username: `admin`
- Password: (output from command above)

---

## 5. Check Application Status

In ArgoCD UI, verify `agri-curve-app` shows:
- Status: Healthy + Synced
- CronJob scheduled for 12:00 daily

Or via CLI:
```bash
kubectl get cronjob,service -n default
```

---

## 6. Manual Pipeline Trigger (Testing)

```bash
kubectl create job test-manual --from=cronjob/agri-curve-cronjob
kubectl logs -l job-name=test-manual -f
```

Check output files:
```bash
ls -la data/processed/
```

Cleanup test job:
```bash
kubectl delete job test-manual
```

---

## Quick Reference Commands

### Check what's running
```bash
kubectl get pods -A
kubectl get cronjob,service -n default
```

### View CronJob schedule
```bash
kubectl get cronjob agri-curve-cronjob
```

### Check recent jobs
```bash
kubectl get jobs -n default
```

### View application logs
```bash
kubectl logs -l app=agri-curve --tail=100
```

### View logs from specific job
```bash
kubectl get jobs
kubectl logs -l job-name=<job-name> --all-containers=true
```

### Restart minikube (if issues)
```bash
minikube stop
minikube start
```

---

## Stopping for the Day

1. Close ArgoCD port-forward terminal (Ctrl+C)
2. Close minikube mount terminal (Ctrl+C)
3. Stop minikube:
   ```bash
   minikube stop
   ```

**Note:** Don't delete minikube cluster. Just stop it to preserve all configuration.

---

## Troubleshooting

### ArgoCD shows OutOfSync
Click SYNC button in UI with PRUNE and FORCE options enabled.

Or via CLI:
```bash
kubectl patch application agri-curve-app -n argocd -p '{"metadata":{"finalizers":null}}' --type=merge
kubectl delete application agri-curve-app -n argocd
kubectl apply -f argocd-application.yaml
```

### Files not appearing in data/processed/
Verify mount terminal is running. Restart mount if needed.

Check if mount is active:
```bash
minikube ssh
ls -la /mnt/agri-data
exit
```

### CronJob not running
Check schedule:
```bash
kubectl describe cronjob agri-curve-cronjob
```

Runs daily at 12:00 Brasília time. Use manual trigger for testing.

### Can't access ArgoCD UI
Verify port-forward is running:
```bash
ps aux | grep "port-forward"
```

Kill existing and restart:
```bash
pkill -f "port-forward.*argocd"
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### Pod crashes or errors
View pod logs:
```bash
kubectl get pods -n default
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Need to rebuild and push new image
```bash
docker build -t nsboan/agri-curve:v<new-version> .
docker push nsboan/agri-curve:v<new-version>
```

Update deployment.yaml with new image tag, commit and push to Git.

---

## Terminal Setup Summary

You need **3 terminals** running simultaneously:

**Terminal 1 - Volume Mount (must stay open):**
```bash
cd ~/projetos/agri-curve
minikube mount $(pwd)/data/processed:/mnt/agri-data
```

**Terminal 2 - ArgoCD Port Forward (must stay open):**
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

**Terminal 3 - Working Terminal:**
Use for kubectl commands, git operations, docker builds, etc.
```

Copy everything above and save to `STARTUP.md` in your project root.
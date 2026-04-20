# PCAI Chat Demo

A minimal Gradio chat interface deployable as a **Framework** on [HPE Private Cloud AI (PCAI)](https://www.hpe.com/us/en/private-cloud-ai.html).  
It connects to any OpenAI-compatible LLM endpoint (e.g. PCAI MLIS) and lets you chat in the browser.

---

## Repository structure

```
pcai-chat-demo/
├── app/
│   ├── app.py              # Gradio chat UI (Python)
│   └── requirements.txt
├── docker/
│   ├── Dockerfile
│   └── build.sh            # Build & push container image
├── helm/
│   └── pcai-chat-demo/     # Helm chart
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── serviceaccount.yaml
│           └── ezua/
│               ├── virtualService.yaml   # Istio routing for PCAI
│               └── Kyverno.yaml          # PCAI pod labels
├── package.sh              # helm package convenience script
└── README.md
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Docker | any recent |
| Helm | 3.x |
| Access to a container registry | (Docker Hub, Harbor, …) |
| HPE PCAI cluster | with a deployed LLM via MLIS |

---

## Step 1 — Build and push the Docker image

Edit `docker/build.sh` and set `IMAGE_REPO` to your registry/repo, then:

```bash
bash docker/build.sh
```

Update `helm/pcai-chat-demo/values.yaml` → `image.repository` / `image.tag` to match.

---

## Step 2 — Package the Helm chart

```bash
bash package.sh
# produces pcai-chat-demo-0.1.0.tgz in the repo root
```

---

## Step 3 — Import into PCAI

1. Log in to the PCAI console and navigate to your **shared project**.
2. Go to **Tools & Frameworks → Import Framework**.
3. Enter a name and description, then upload `pcai-chat-demo-0.1.0.tgz`.
4. In the **values editor**, set:

   ```yaml
   ezua:
     virtualService:
       endpoint: "pcai-chat-demo.<namespace>.ingress.<cluster-domain>"
       istioGateway: "istio-system/ezaf-gateway"

   env:
     LLM_ENDPOINT: "https://mlis.<namespace>.ingress.<cluster-domain>/v1"
     LLM_API_KEY: "<your-api-key>"      # leave blank if not required
     LLM_MODEL: "meta-llama/Llama-3.1-8B-Instruct"
   ```

5. Click **Deploy**. The app will appear as a tile in the shared project.

---

## Configuration reference

| Value | Description | Default |
|-------|-------------|---------|
| `image.repository` | Container image | `docker.io/your-dockerhub-username/pcai-chat-demo` |
| `image.tag` | Image tag | `0.1.0` |
| `env.LLM_ENDPOINT` | OpenAI-compatible base URL | `""` |
| `env.LLM_API_KEY` | API key | `""` |
| `env.LLM_MODEL` | Model name | `""` |
| `env.SYSTEM_PROMPT` | System prompt | (generic PCAI assistant) |
| `ezua.virtualService.endpoint` | FQDN for PCAI routing | `pcai-chat-demo.${DOMAIN_NAME}` |
| `ezua.virtualService.istioGateway` | Istio gateway | `istio-system/ezaf-gateway` |

> **Note:** `LLM_ENDPOINT`, `LLM_API_KEY`, and `LLM_MODEL` can also be set interactively in the Gradio UI at runtime without redeploying.

---

## References

- [HPE PCAI — Managing Application Lifecycle](https://support.hpe.com/hpesc/public/docDisplay?docId=a00aie18hen_us&page=ManageClusters/managing-application-lifecycle.html)
- [HPE ai-solution-eng/frameworks](https://github.com/ai-solution-eng/frameworks) — canonical PCAI Helm chart examples
- [Gradio docs](https://www.gradio.app/docs)

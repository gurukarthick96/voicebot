envsubst < azure-pipelines/k8s.secrets.template.yaml | kubectl apply -f -

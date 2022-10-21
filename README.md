# azureblob-to-azureblob
Copies Files from Azure Blob Storage to another Azure Blob Storage

# Deployment and Usage
Deployment via `kustomization.yaml`
```
bases:
  - github.com/binkhq/azureblob-to-azureblob/deploy

patches:
  - target:
      kind: CronJob
    patch: |-
      - op: replace
        path: /metadata/name
        value: media-daily-backup
  - target:
      kind: CronJob
    patch: |-
      - op: replace
        path: /spec/schedule
        value: "0 1 * * *"
  - target:
      kind: CronJob
    patch: |-
      - op: replace
        path: /spec/jobTemplate/spec/template/spec/containers/0/env
        value:
          - name: source_connection_string
            valueFrom:
              secretKeyRef:
                key: connection_string
                name: azure-storage-common
          - name: destination_connection_string
            valueFrom:
              secretKeyRef:
                key: connection_string
                name: azure-storage-common
          - name: source_container_name
            value: media
          - name: destination_container_name
            value: backups
```

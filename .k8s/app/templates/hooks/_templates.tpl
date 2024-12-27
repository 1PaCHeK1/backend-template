{{- define "hooks.labels" }}
{{ include "common.labels" . }}
app.kubernetes.io/component: hooks
{{- end }}

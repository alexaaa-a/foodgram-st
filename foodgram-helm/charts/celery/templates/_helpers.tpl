{{- define "celery.labels" -}}
app.kubernetes.io/name: {{ include "celery.name" . }}
helm.sh/chart: {{ include "celery.chart" . }}
{{- with .Chart.AppVersion }}
app.kubernetes.io/version: {{ . }}
{{- end }}
{{- if .Values.global.environment }}
environment: {{ .Values.global.environment }}
{{- end }}
{{- end }}

{{- define "celery.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "celery.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

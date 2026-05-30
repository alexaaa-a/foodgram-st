{{- define "jobs.labels" -}}
app.kubernetes.io/name: {{ include "jobs.name" . }}
helm.sh/chart: {{ include "jobs.chart" . }}
{{- with .Chart.AppVersion }}
app.kubernetes.io/version: {{ . }}
{{- end }}
{{- if .Values.global.environment }}
environment: {{ .Values.global.environment }}
{{- end }}
{{- end }}

{{- define "jobs.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "jobs.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

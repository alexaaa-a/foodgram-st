{{- define "backend.labels" -}}
app.kubernetes.io/name: {{ include "backend.name" . }}
helm.sh/chart: {{ include "backend.chart" . }}
{{- with .Chart.AppVersion }}
app.kubernetes.io/version: {{ . }}
{{- end }}
{{- if .Values.global.environment }}
environment: {{ .Values.global.environment }}
{{- end }}
{{- end }}

{{- define "backend.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "backend.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

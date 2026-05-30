{{- define "nginx.labels" -}}
app.kubernetes.io/name: {{ include "nginx.name" . }}
helm.sh/chart: {{ include "nginx.chart" . }}
{{- with .Chart.AppVersion }}
app.kubernetes.io/version: {{ . }}
{{- end }}
{{- if .Values.global.environment }}
environment: {{ .Values.global.environment }}
{{- end }}
{{- end }}

{{- define "nginx.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "nginx.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

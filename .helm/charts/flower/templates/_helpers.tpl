{{- define "flower.labels" -}}
app.kubernetes.io/name: {{ include "flower.name" . }}
helm.sh/chart: {{ include "flower.chart" . }}
{{- with .Chart.AppVersion }}
app.kubernetes.io/version: {{ . }}
{{- end }}
{{- if .Values.global.environment }}
environment: {{ .Values.global.environment }}
{{- end }}
{{- end }}

{{- define "flower.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "flower.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

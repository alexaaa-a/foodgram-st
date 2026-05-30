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

{{- define "flower.backendImage" -}}
{{- if and .Values.werfImage (not (contains "{{" .Values.werfImage)) -}}
{{- .Values.werfImage -}}
{{- else if and .Values.werf .Values.werf.image.backend -}}
{{- .Values.werf.image.backend -}}
{{- else -}}
{{- printf "%s:%s" .Values.global.image.backend.repository .Values.global.image.backend.tag -}}
{{- end -}}
{{- end }}

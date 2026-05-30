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

{{- define "celery.backendImage" -}}
{{- if and .Values.werfImage (not (contains "{{" .Values.werfImage)) -}}
{{- .Values.werfImage -}}
{{- else if and .Values.werf .Values.werf.image.backend -}}
{{- .Values.werf.image.backend -}}
{{- else -}}
{{- printf "%s:%s" .Values.global.image.backend.repository .Values.global.image.backend.tag -}}
{{- end -}}
{{- end }}

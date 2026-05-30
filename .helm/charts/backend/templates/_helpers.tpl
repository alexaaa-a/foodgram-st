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

{{- define "backend.image" -}}
{{- if and .Values.werfImage (not (contains "{{" .Values.werfImage)) -}}
{{- .Values.werfImage -}}
{{- else if and .Values.werf .Values.werf.image.backend -}}
{{- .Values.werf.image.backend -}}
{{- else -}}
{{- printf "%s:%s" .Values.global.image.backend.repository .Values.global.image.backend.tag -}}
{{- end -}}
{{- end }}

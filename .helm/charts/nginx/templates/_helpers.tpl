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

{{- define "nginx.image" -}}
{{- if and .Values.werfImage (not (contains "{{" .Values.werfImage)) -}}
{{- .Values.werfImage -}}
{{- else if and .Values.werf .Values.werf.image.frontend -}}
{{- .Values.werf.image.frontend -}}
{{- else -}}
{{- printf "%s:%s" .Values.global.image.frontend.repository .Values.global.image.frontend.tag -}}
{{- end -}}
{{- end }}

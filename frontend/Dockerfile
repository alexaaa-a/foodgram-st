FROM node:21.7.1-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . ./
RUN npm run build
FROM alpine:latest
WORKDIR /static_build
COPY --from=builder /app/build ./

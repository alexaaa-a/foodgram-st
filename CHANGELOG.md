# [1.2.0](https://github.com/alexaaa-a/foodgram-st/compare/v1.1.0...v1.2.0) (2026-06-02)


### Bug Fixes

* **grafana:** remove unused files ([34e25b1](https://github.com/alexaaa-a/foodgram-st/commit/34e25b154d65f156f5a55d38ccd02c71a0cd42c6))
* **monitoring:** enable ingress-nginx metrics and update metric name in docs ([93b7623](https://github.com/alexaaa-a/foodgram-st/commit/93b7623db368b66e9f4951ff9a1f3f1850a06c36))
* **monitoring:** increase helmfile timeout and fix nginx scrape relabel ([b727be7](https://github.com/alexaaa-a/foodgram-st/commit/b727be760273f96b62e271d98a07cc51a27be303))
* **monitoring:** move Grafana SMTP credentials to Kubernetes secret ([06366be](https://github.com/alexaaa-a/foodgram-st/commit/06366be7c5ae8c36e237835bc6f02dddd81bc82b))
* **monitoring:** remove rewrite-target from prometheus ingress, fix hosts docs ([96960ac](https://github.com/alexaaa-a/foodgram-st/commit/96960ac33b5ed0c579fc0e7f3a1ec5b85e54b747))


### Features

* **monitoring:** add helmfile stack — Prometheus, Loki, Promtail, Grafana ([6339e98](https://github.com/alexaaa-a/foodgram-st/commit/6339e983b94f39b5d9548e6552b816b8e882afec))

# [1.1.0](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.8...v1.1.0) (2026-06-02)


### Bug Fixes

* **ci:** checkout main before helm values auto-commit ([5e6c1bf](https://github.com/alexaaa-a/foodgram-st/commit/5e6c1bf1146e351e78570a097faae0a377e60387))
* **ci:** reuse docker login on self-hosted runner, add retries ([b46f9c3](https://github.com/alexaaa-a/foodgram-st/commit/b46f9c38613f22bda1a8ac88e80390d40224913b))
* disable RabbitMQ sidecars blocking django deployment ([c416109](https://github.com/alexaaa-a/foodgram-st/commit/c4161090103433189e495896686d48e183dd33d0))
* **redis:** pass vault password and fix requirepass ([d78ee6d](https://github.com/alexaaa-a/foodgram-st/commit/d78ee6d2856fa5c5d59314aa12b02d4750fd888f))
* **werf:** add frontend dockerignore and fix dockerfile paths ([2307176](https://github.com/alexaaa-a/foodgram-st/commit/23071762af9d945dff50f8fc88a60659a88b3557))
* **werf:** correct dockerfile paths and set default repo ([3fe5956](https://github.com/alexaaa-a/foodgram-st/commit/3fe5956eb6b1d6b39e64dc7e0aaea07abce700a9))
* **werf:** exclude locust config from backend build context ([50b3d17](https://github.com/alexaaa-a/foodgram-st/commit/50b3d171b310cc026a4c6a8f16ff5f3a1627318a))
* **werf:** ignore .DS_Store in frontend build context ([11a688b](https://github.com/alexaaa-a/foodgram-st/commit/11a688b3b1bbe04a64ef314864d023beae1286b0))
* **werf:** in-cluster vault addr for pods, fix jobs env ([45cc2b2](https://github.com/alexaaa-a/foodgram-st/commit/45cc2b22c88bfece88c11448df2e00955174d227))
* **werf:** pass werf images to subcharts, arm64 build, redis password ([f5e4664](https://github.com/alexaaa-a/foodgram-st/commit/f5e466471ec05f4f31a5ecbe719e502fa8f9b791))
* **werf:** remove namespace from chart, created by deploy script ([c95248a](https://github.com/alexaaa-a/foodgram-st/commit/c95248ab0c97fc121573113517176e917b4eb85e))
* **werf:** remove orphan actions-runner chart causing namespace conflict ([07ad28e](https://github.com/alexaaa-a/foodgram-st/commit/07ad28e84af75e2372152cb4935ad630fb2f3637))
* **werf:** render werf image templates correctly in values.yaml ([3856c1f](https://github.com/alexaaa-a/foodgram-st/commit/3856c1fd0acc72be6122e4e0d0d5b833c69ac0d3))
* **werf:** use full frontend Dockerfile for werf build ([9c8b0b2](https://github.com/alexaaa-a/foodgram-st/commit/9c8b0b23f8042a0b29f8c17dfc6110012120755b))
* **werf:** use global.werf.images instead of templated values.yaml ([6b1effa](https://github.com/alexaaa-a/foodgram-st/commit/6b1effaae797a13dbf4e4cb10265bc7a90a41c35))


### Features

* **werf:** add werf config, helm refactor, vault integration ([aa01eed](https://github.com/alexaaa-a/foodgram-st/commit/aa01eedccbb4870106d54c83a653b5caca60802d))

## [1.0.10](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.9...v1.0.10) (2026-05-30)


### Bug Fixes

* **ci:** checkout main before helm values auto-commit ([b7d0e2e](https://github.com/alexaaa-a/foodgram-st/commit/b7d0e2e802e1a214e0280931d7c2ca69d250ed2f))

## [1.0.9](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.8...v1.0.9) (2026-05-30)


### Bug Fixes

* **ci:** reuse docker login on self-hosted runner, add retries ([b46f9c3](https://github.com/alexaaa-a/foodgram-st/commit/b46f9c38613f22bda1a8ac88e80390d40224913b))

## [1.0.8](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.7...v1.0.8) (2026-05-30)


### Bug Fixes

* **ci:** fix css flex-end values and allow frontend build on self-hosted runner ([96af4d5](https://github.com/alexaaa-a/foodgram-st/commit/96af4d5c708860031c1a55862b18f15e71690294))

## [1.0.7](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.6...v1.0.7) (2026-05-30)


### Bug Fixes

* **ci:** disable eslint plugin during frontend build on runner ([74ea842](https://github.com/alexaaa-a/foodgram-st/commit/74ea842b72b383fa08d741b0093cd8e0f7525f39))

## [1.0.6](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.5...v1.0.6) (2026-05-30)


### Bug Fixes

* **ci:** build frontend on self-hosted runner, pack static into nginx image ([4180f31](https://github.com/alexaaa-a/foodgram-st/commit/4180f31492d798ddc9555db6587785e15a45d3e4))

## [1.0.5](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.4...v1.0.5) (2026-05-30)


### Bug Fixes

* limits ([36d74b9](https://github.com/alexaaa-a/foodgram-st/commit/36d74b9e4820f3fdeee2075518515a3789f584d4))

## [1.0.4](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.3...v1.0.4) (2026-05-30)


### Bug Fixes

* verify automatic docker build ([1f219ca](https://github.com/alexaaa-a/foodgram-st/commit/1f219cadfc7a956e11522475918530ca1b8ac10f))

## [1.0.3](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.2...v1.0.3) (2026-05-30)


### Bug Fixes

* **ci:** docker build on self-hosted runner and auto trigger on release ([685e25f](https://github.com/alexaaa-a/foodgram-st/commit/685e25f0eb70a262bddec0fefeea48b3385a954d))

## [1.0.2](https://github.com/alexaaa-a/foodgram-st/compare/v1.0.1...v1.0.2) (2026-05-30)


### Bug Fixes

* **ci:** match semver tags with v* pattern for Docker workflows ([6b2ad56](https://github.com/alexaaa-a/foodgram-st/commit/6b2ad5611caea46a0b4664e7b199f51188572bc3))

# 1.0.0 (2026-05-30)


### Features

* add CI/CD pipeline with semantic-release and self-hosted runner ([a744c34](https://github.com/alexaaa-a/foodgram-st/commit/a744c34827585c879407f1f74e55e38a9132e9dc))
* add package-lock.json ([0b4c536](https://github.com/alexaaa-a/foodgram-st/commit/0b4c5368f2cbe5aabc858abc3fb0e645355173ae))

# 🚀 CI/CD с Kubernetes и Helm

Учебный DevOps-проект, демонстрирующий автоматизацию тестирования, сборки Docker-образов и развертывания FastAPI-приложения в Kubernetes с использованием GitHub Actions и Helm.

Проект реализует CI/CD pipeline, управление несколькими окружениями, Rolling Update и возможность отката приложения к предыдущей версии.

## 📌 О проекте

Цель проекта — построить автоматизированный процесс доставки приложения от исходного кода до работающего Kubernetes-кластера.

При каждом push в ветку `main` автоматически запускается pipeline, который:

1. Получает исходный код из GitHub.
2. Устанавливает зависимости Python.
3. Запускает автоматические тесты с помощью pytest.
4. Собирает Docker-образ приложения.
5. Публикует Docker-образ в GitHub Container Registry (GHCR).
6. Развертывает новую версию приложения в Kubernetes с помощью Helm.
7. Проверяет успешность развертывания.

## 🛠 Используемые технологии

| Технология | Назначение |
|---|---|
| Linux (Kali Linux) | Среда разработки и выполнения |
| Python 3.12 | Язык программирования |
| FastAPI | Backend-приложение |
| pytest | Автоматическое тестирование |
| Docker | Контейнеризация приложения |
| Kubernetes | Оркестрация контейнеров |
| Minikube | Локальный Kubernetes-кластер |
| Helm | Управление Kubernetes-манифестами |
| GitHub Actions | Автоматизация CI/CD |
| GitHub Container Registry | Хранение Docker-образов |
| kubectl | Управление Kubernetes |

## 🏗 Архитектура проекта

```text
                 Developer
                     |
                     v
               Git Push (main)
                     |
                     v
              GitHub Repository
                     |
                     v
              GitHub Actions
                     |
          +----------+----------+
          |                     |
          v                     |
      Run Tests                 |
       (pytest)                 |
          |                     |
          v                     |
      Build Docker Image        |
          |                     |
          v                     |
       Push to GHCR              |
          |                     |
          v                     |
      Kubernetes Deploy <-------+
          |
          v
       Helm Upgrade
          |
          v
     Kubernetes Cluster
          |
       +--+--+
       |     |
       v     v
      Dev   Prod
       |     |
       v     v
    FastAPI FastAPI
     Pods    Pods
       |     |
       +--+--+
          |
          v
       Services
```

## 📁 Структура репозитория

```text
devops2-kubernetes-cicd/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

## ⚙️ Функциональность приложения

Приложение построено на FastAPI и предоставляет три HTTP endpoint.

| Endpoint | Описание |
|---|---|
| `GET /` | Главная страница приложения |
| `GET /health` | Проверка состояния приложения |
| `GET /info` | Информация о приложении и его версии |

Пример ответа `/`:

```json
{
  "message": "Hello from Kubernetes CI/CD project! Version 2.0",
  "status": "running"
}
```

Пример ответа `/health`:

```json
{
  "status": "healthy"
}
```

Пример ответа `/info`:

```json
{
  "application": "Kubernetes CI/CD Demo",
  "version": "2.0.0",
  "timestamp": "2026-11-24T12:00:00+00:00"
}
```

## 🔄 CI/CD Pipeline

Автоматизация реализована с помощью GitHub Actions.

Workflow находится в файле:

```text
.github/workflows/ci-cd.yml
```

### Этап 1. Тестирование

При push или pull request в ветку `main` запускается job `test`.

Выполняются следующие действия:

- Получение исходного кода.
- Установка Python 3.12.
- Установка зависимостей из `requirements.txt`.
- Запуск pytest.

Если тесты завершаются ошибкой, дальнейшая сборка и публикация Docker-образа не выполняются.

### Этап 2. Сборка Docker-образа

После успешного прохождения тестов GitHub Actions:

- Настраивает Docker Buildx.
- Авторизуется в GitHub Container Registry.
- Собирает Docker-образ.
- Публикует образ в GHCR.

Для каждого коммита создаются два тега:

```text
latest
<commit-sha>
```

Использование SHA-тега позволяет точно определить версию приложения и обеспечивает возможность возврата к предыдущей сборке.

### Этап 3. Развертывание

После публикации Docker-образа запускается job `deploy`.

Развертывание выполняется на self-hosted GitHub Actions runner, который имеет доступ к локальному Kubernetes-кластеру Minikube.

Для установки и обновления приложения используется Helm:

```bash
helm upgrade --install fastapi ./helm \
  --namespace dev \
  --set image.repository=ghcr.io/cursedocks/devops2-kubernetes-cicd \
  --set-string image.tag=${GITHUB_SHA} \
  --wait \
  --atomic \
  --timeout 180s
```

После развертывания проверяется состояние Deployment и Pod:

```bash
kubectl rollout status deployment/fastapi-deployment -n dev
kubectl get pods -n dev
```



## Переменные окружения

Использую [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

### Локально

Секреты сохраняются в файле `secrets.toml`.

```bash
.streamlit/secrets.toml
```

### Streamlit Cloud

`App Settings → Secrets` → вставить содержимое `secrets.toml.example` с реальными значениями.

| Переменная    | Откуда                          |
| ------------- | ------------------------------- |
| `FIGMA_TOKEN` | Figma → Personal access tokens  |
| `APP_ENV`     | `dev` локально, `prod` в облаке |

# LocalCloud ☁️
**LocalCloud** — современная и асинхронная Python-библиотека для удобного локального обмена данными между устройствами.

---

## ⚡ Возможности и Примеры

Библиотека разделена на специализированные менеджеры:

| Менеджер | Описание | Пример кода |
| :--- | :--- | :---: |
| 📁 **FileManager** | Передача одиночных файлов и целых папок с сохранением структуры | [FileManager.py](examples/Managers/FileManager/FileManagerExample.py) |
| 🔔 **EventsManager** | Генерация и обработка пользовательских событий в локальной сети | [EventsManager.py](examples/Managers/EventsManager/EventsManagerExample.py) |
| ⚡ **FunctionsManager** | Удаленный вызов функций (RPC) с фильтрацией и возвратом ответа | [FunctionsManager.py](examples/Managers/FunctionsManager/FunctionsManagerExample.py) |
| 📦 **VariablesManager** | Распределенное синхронное/асинхронное состояние переменных | [VariablesManager.py](examples/Managers/VariablesManager/VariablesManagerExample.py) |

---

## 🛡️ Безопасность данных

> [!IMPORTANT]
> **Push-Only архитектура:** Все основные методы библиотеки работают исключительно в формате **односторонней отправки**. Другое устройство не может самовольно прочитать данные с вашего ПК.

#### ⚠️ Исключения из правила:
* **VariablesManager:** Если на вашей стороне открыт доступ к конкретным переменным.
* **FunctionsManager:** Если явный обработчик функции задекларирован с возвратом значения (`return`).

---

## 📦 Установка

Установка напрямую из GitHub-репозитория:

```bash
pip install git+https://github.com/Kir1ll-K-Labs/LocalCloud.git
```

[![Download ZIP](https://img.shields.io/badge/Скачать_.ZIP_проект-2ea44f?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Kir1ll-K-Labs/LocalCloud/archive/refs/heads/main.zip)

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT**. Подробнее см. в файле [LICENSE](LICENSE).

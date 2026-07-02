# POST /users — создание пользователя
Тело:
```jsonc
{
  "name": "foksik",
  "password": "P8iLFx5IjxMTeSkx"
}
```

Ответ (201 USER_CREATED):
```jsonc
{
  "id": "019f08b4-e6f1-7fea-95e3-4507dc543832", // UUID человека
  "name": "foksik", // Ник человека
  "groups": ["default"], // Группы привелегий
  "password": null, // Строка, хеш пароля в argon2
  "permissions": {"svc-users":["create"]}, // Права которые накладываются поверх групп
  "createdAt": "2026-06-26T03:00:44.053Z", // Дата создания аккаунта
  "updatedAt": "2026-06-26T03:00:44.053Z" // Дата последнего изменения (ника, групп, прав)
}
```

Возможные ошибки:
- 400, USER_INVALID_DATA — если имя пользователя или пароль отсутствуют или пусты
- 400, USER_DUPLICATE — пользователь с таким именем уже существует

# GET /users/:idOrName — получение информации по 1 пользователю
Query:
- psw=<true/false> — добавляет поле password к ответу (argon2 хеш пароля)

Ответ (200 USER_FETCHED_OK):
```jsonc
{
  "id": "019f08b4-e6f1-7fea-95e3-4507dc543832",
  "name": "foksik",
  "groups": ["default"],
  "permissions": {"svc-users":["create"]},
  "createdAt": "2026-06-26T03:00:44.053Z",
  "updatedAt": "2026-06-26T03:00:44.053Z"
}
```

Возможные ошибки:
- 500, USER_INTERNAL_ERROR — если какая-то критическая ошибка там (практически невозможно)
- 400, USER_INVALID_DATA — если idOrName пуст или отсутствует
- 404, USER_NOT_FOUND — если пользователь не найден

# GET /users/:idOrName/permissions — получение суммарных прав пользователя
Query:
- servicename=<имя сервиса типо svc-users> — имя сервера **ОБЯЗАТЕЛЬНО**

Ответ (200 USER_FETCHED_OK):
```jsonc
[
  "create",
  "read_password",
  "delete"
]
```

Возможные ошибки:
- 500, USER_INTERNAL_ERROR — если какая-то критическая ошибка там (практически невозможно)
- 400, USER_INVALID_DATA — если idOrName пуст или отсутствует
- 404, USER_NOT_FOUND — если пользователь не найден

# GET /users/me — получение информации по текущему пользователю (требует чтобы запрос пришел от user-а с авторизацией, через gateway)
Ответ (200 USER_FETCHED_OK):
```jsonc
{
  "id": "019f08b4-e6f1-7fea-95e3-4507dc543832",
  "name": "foksik",
  "groups": ["default"],
  "permissions": {"svc-users":["create"]},
  "createdAt": "2026-06-26T03:00:44.053Z",
  "updatedAt": "2026-06-26T03:00:44.053Z"
}
```

Возможные ошибки:
- 500, USER_INTERNAL_ERROR — если какая-то критическая ошибка там
- 400, USER_INVALID_DATA — если почему-то не передался userId
- 404, USER_NOT_FOUND — если пользователь не найден

# GET /users — поиск по пользователям
Query:
- search — строка по которой мы исщем
- page — номер страницы на которой мы смотрим
- limit — лимит пользователей на 1 странице

Ответ 200, USER_LIST_FETCHED (+ данные пагинации как в [API Guidelines](https://github.com/FreedomDevs/API_Guidelines/blob/main/README.md#%D0%BF%D0%B0%D0%B3%D0%B8%D0%BD%D0%B0%D1%86%D0%B8%D1%8F)):
```jsonc
{
  "users": [
    {
      "id": "019f08b4-e6f1-7fea-95e3-4507dc543832",
      "name": "foksik",
      "groups": ["default"],
      "permissions": {"svc-users":["create"]},
      "createdAt": "2026-06-26T03:00:44.053Z",
      "updatedAt": "2026-06-26T03:00:44.053Z"
    }
    //...
  ]
}
```

Возможные ошибки:
- 400, USER_INVALID_PAGINATION — если page или limit неправильные какие-то

# DELETE /users/:idOrName — удаляет пользователя
Ответ 200, USER_DELETED, без data

Возможные ошибки:
- 400, USER_INVALID_DATA — если почему-то не передался userId
- 404, USER_NOT_FOUND — если пользователь не найден

# PUT /users/:idOrName/permissions — заменяет права пользователя
Ответ 200, PERMISSIONS_UPDATED:
```jsonc
{
  "groups": ["default", "admin"],
  "permissions": {"svc-users":["read_password","read"]}
}
```

Возможные ошибки:
- 400, USER_INVALID_DATA — если почему-то не передался userId
- 404, USER_NOT_FOUND — если пользователь не найден

# PUT /users/:idOrName/password — заменяет права пользователя
Тело:
```jsonc
{
  "password": "P8iLFx5IjxMTeSkx"  //Новый пароль для замены
}
```
Ответ 200, PASSWORD_UPDATED:
```jsonc
{
  "password": "P8iLFx5IjxMTeSkx" //Новый пароль
}
```

Возможные ошибки:
- 400, USER_INVALID_DATA — если почему-то не передался userId
- 404, USER_NOT_FOUND — если пользователь не найден

# PUT /users/:idOrName/name — заменяет права пользователя
Тело:
```jsonc
{
  "name": "foksik" //Новый Name(login) для замены
}
```
Ответ 200, NAME_UPDATED:
```jsonc
{
  "name": "foksik" //Новый Name(login)
}
```

Возможные ошибки:
- 400, USER_INVALID_DATA — если почему-то не передался userId
- 404, USER_NOT_FOUND — если пользователь не найден

# POST /groups — создаёт новую группу
Запрос:
```jsonc
{
  "name": "admin"
}
```

Ответ 200, GROUP_CREATED:
```jsonc
{
  "id": "019f08ee-9f3e-7c94-b899-19675e041af8",
  "name": "admin",
  "permissions": {"svc-users":["read_password","read"]},
  "users": [],
  "createdAt": "2026-06-26T03:00:44.053Z",
  "updatedAt": "2026-06-26T03:00:44.053Z"
}
```

Возможные ошибки:
- 400, GROUP_ALREADY_EXISTS — если группа с таким названием уже существует

# DELETE /groups/:idOrName — удаляет группу
Ответ 200, GROUP_DELETED:
```jsonc
{
  "id": "019f08ee-9f3e-7c94-b899-19675e041af8",
  "name": "admin",
  "permissions": {"svc-users":["read_password","read"]},
  "users": ["019f08b4-e6f1-7fea-95e3-4507dc543832"],
  "createdAt": "2026-06-26T03:00:44.053Z",
  "updatedAt": "2026-06-26T03:00:44.053Z"
}
```

Возможные ошибки:
- 404, GROUP_NOT_FOUND — если группа не найдена

# GET /groups — возвращает список групп
Ответ 200, GROUP_FETCHED:
```jsonc
[
  {
    "id": "019f08ee-9f3e-7c94-b899-19675e041af8",
    "name": "admin",
    "permissions": {"svc-users":["read_password","read"]},
    "users": ["019f08b4-e6f1-7fea-95e3-4507dc543832"],
    "createdAt": "2026-06-26T03:00:44.053Z",
    "updatedAt": "2026-06-26T03:00:44.053Z"
  }
  //...
]
```

# PUT /groups/permissions
Запрос:
```jsonc
{
  "permissions": {"svc-users":["read","create","delete"]}
}
```

Ответ 200, GROUP_PERMISSIONS_UPDATED:
```jsonc
{
    "id": "019f08ee-9f3e-7c94-b899-19675e041af8",
    "name": "admin",
    "permissions": {"svc-users":["read","create","delete"]},
    "users": ["019f08b4-e6f1-7fea-95e3-4507dc543832"],
    "createdAt": "2026-06-26T03:00:44.053Z",
    "updatedAt": "2026-06-26T03:00:44.053Z"
}
```

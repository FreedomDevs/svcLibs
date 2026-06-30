# POST /auth/register — Регистрация
Запрос:
```jsonc
{
  "login": "foks",
  "password": "XatsLPheo4rcQGtfcky1xXScEtFThFJkfdZ7xpXnYp5yLLSB",
  "email": "почта"
}
```

Ответ 201, REGISTRATION_SUCCESS:
```jsonc
{
  "email_verefication_token": "kMsAsAqJ9WY="
}
```

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 500, HASHING_FAILED — ошибка при генерации хеша

# POST /auth/confirm_email — Подтверждение почты
Запрос:
```jsonc
{
  "email_verefication_token": "kMsAsAqJ9WY=",
  "code": 123641
}
```

Ответ 201, REGISTRATION_SUCCESS:
```jsonc
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.OYkcX0_sy5JLWoEOrVkzajdLIB52q1550J411XzBgBk", // JWT токен подписаный svc-auth
  "refresh_token": "UUE5SmZ1T2JPYW9RT2FpOFE1VUxudm9mcWlPWm1RaG9lVWRFaE9YUW4yR0NyVnJnV3BXQTgydTd6eDRKMjJWSQo=" // Случайная фигня в base64
}
```

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 500, HASHING_FAILED — ошибка при генерации хеша

# POST /auth/resend_email — Переотправка почты
Запрос:
```jsonc
{
  "email_verefication_token": "kMsAsAqJ9WY=",
}
```

Ответ 201, RESEND_SUCCESS, без тела

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 500, HASHING_FAILED — ошибка при генерации хеша

# POST /auth/alt/register — Альт регистрация (без access_token-а)
Запрос:
```jsonc
{
  "login": "foks",
  "password": "XatsLPheo4rcQGtfcky1xXScEtFThFJkfdZ7xpXnYp5yLLSB"
}
```

Ответ 201, REGISTRATION_SUCCESS:
```jsonc
{
  "refresh_token": "UUE5SmZ1T2JPYW9RT2FpOFE1VUxudm9mcWlPWm1RaG9lVWRFaE9YUW4yR0NyVnJnV3BXQTgydTd6eDRKMjJWSQo=" // Случайная фигня в base64
}
```

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 500, HASHING_FAILED — ошибка при генерации хеша

# POST /auth/login — Вход в аккаунт
Запрос:
```jsonc
{
  "login": "foks",
  "password": "XatsLPheo4rcQGtfcky1xXScEtFThFJkfdZ7xpXnYp5yLLSB"
}
```

Ответ 200, AUTH_SUCCESS если подчта подтверждена:
```jsonc
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.OYkcX0_sy5JLWoEOrVkzajdLIB52q1550J411XzBgBk", // JWT токен подписаный svc-auth
  "refresh_token": "UUE5SmZ1T2JPYW9RT2FpOFE1VUxudm9mcWlPWm1RaG9lVWRFaE9YUW4yR0NyVnJnV3BXQTgydTd6eDRKMjJWSQo=" // Случайная фигня в base64
}
```

Ответ 401, EMAIL_NOT_SET если почты нет:
```jsonc
{
  "email_verefication_token": "kMsAsAqJ9WY=",
}
```

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 401, PASSWORD_INVALID — Неправильный пароль
- 404, USER_NOT_FOUND — Если пользователь с таким логином не найден

# POST /auth/alt/login — Альт вход в аккаунт (без access_token-а)
Запрос:
```jsonc
{
  "login": "foks",
  "password": "XatsLPheo4rcQGtfcky1xXScEtFThFJkfdZ7xpXnYp5yLLSB"
}
```

Ответ 200, AUTH_SUCCESS:
```jsonc
{
  "refresh_token": "UUE5SmZ1T2JPYW9RT2FpOFE1VUxudm9mcWlPWm1RaG9lVWRFaE9YUW4yR0NyVnJnV3BXQTgydTd6eDRKMjJWSQo=" // Случайная фигня в base64
}
```

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 401, PASSWORD_INVALID — Неправильный пароль
- 404, USER_NOT_FOUND — Если пользователь с таким логином не найден

# POST /auth/refresh — Генерирует access_token по refresh_token
Запрос:
```jsonc
{
  "method": "Web", // Генерирует access_token, если сюда вписать Game то он вернёт майнкрафт токен 
  "refresh_token": "UUE5SmZ1T2JPYW9RT2FpOFE1VUxudm9mcWlPWm1RaG9lVWRFaE9YUW4yR0NyVnJnV3BXQTgydTd6eDRKMjJWSQo=" // Случайная фигня в base64
}
```

Ответ 200, AUTH_SUCCESS:
```jsonc
{
  "token": "" // Какой-то токен крч
}
```

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 401, AUTH_FAILED — Не получилось авторизоватся
- 404, USER_NOT_FOUND — Если пользователь с userId из refresh_token не найден (хз когда это возможно)

# POST /auth/check_refresh_token — Проверяет валидность refresh_token-а
Запрос:
```jsonc
{
  "refresh_token": "UUE5SmZ1T2JPYW9RT2FpOFE1VUxudm9mcWlPWm1RaG9lVWRFaE9YUW4yR0NyVnJnV3BXQTgydTd6eDRKMjJWSQo=" // Случайная фигня в base64
}
```

Ответ 200, AUTH_SUCCESS, без тела

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 401, REFRESH_TOKEN_INVALID — Рефрешь токен говно

# POST /auth/pop_game_token — Проверяет game token и удаляет его
Запрос:
```jsonc
{
  "game_token": "lGxtv6EvZ9k=" 
}
```

Ответ 200, AUTH_SUCCESS, без тела

Возможные ошибки:
- 500, USER_CREATION_FAILED — Какая-то странная фигня произошла
- 401, REFRESH_TOKEN_INVALID — Рефрешь токен говно


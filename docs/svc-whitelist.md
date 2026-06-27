# POST /whitelist — Добавление игрока в whitelist
Запрос:
```jsonc
{
  "servername": "test_server", // Если запрос от майнкрафт сервера то servername не нужен
  "userid": "019f08fa-29d4-7f91-9e0e-fee1cd4c6cac"
}
```

Ответ 201, WHITELIST_CREATED_OK, без тела

Возможные ошибки:
- 409, WHITELIST_ALREADY_EXISTS — если этот человек уже в whitelist-е

# GET /whitelist/check — проверка наличия игрока в whitelist
Query:
- userid=019f08fa-29d4-7f91-9e0e-fee1cd4c6cac — id пользователя по которому исщем (обязательно)
- servername=elysium_main — имя сервера на котором исщем (не обязательно вообще, и если запрос идёт от сервера то его имя подставится само)

Ответ если запрос без servername 200, WHITELIST_CHECK_OK:
```jsonc
{
  "userid": "019f08fa-29d4-7f91-9e0e-fee1cd4c6cac",
  "servers": ["elysium_main"]
}
```


Ответ если запрос с servername 200, WHITELIST_CHECK_OK:
```jsonc
{
  "in_whitelist": true
}
```

# DELETE /whitelist
Запрос:
```jsonc
{
  "servername": "test_server", // Если запрос от майнкрафт сервера то servername не нужен
  "userid": "019f08fa-29d4-7f91-9e0e-fee1cd4c6cac"
}
```

Ответ 200, WHITELIST_REMOVED_OK, без data

Возможные ошибки:
- 404, WHITELIST_NOT_FOUND — если такого игрока не было в whitelist

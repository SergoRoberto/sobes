# Добавление функциональности получения данных по протоколу bandwidthtest для средствa lzr.

## Исследования протокола 

Bandwidth-test  - это протокол, используемый измрения пропускной способности канала.

### Имеющиеся материалы

#### Алгоритм работы 

Инициация соединения:
- Клиент устанавливает TCP-соединение с сервером на порт 2000.
- Сервер всегда отвечает 01:00:00:00 
- Клиент отправялет на сервер 16-байтовую команду, начинающуюся с команды 01 (TCP) или 00 (UDP)
    - cmd[0] : Протокол, 01: TCP, 00: UDP
    - cmd[1] : Направление, 01 — передача, 02 — прием, 03 — оба
    - cmd[2] : Случайные данные, 00 — использовать случайные данные; 01 — использовать символ \00
    - cmd[3] : Количество TCP-соединений, 0, если количество TCP-соединений = 1, число, если больше
    - cmd[4:5] : Размер удаленного udp-tx (dc:05) по UDP, 00:80 по TCP
    - cmd[6:7] : Размер клиентского буфера. Максимальное значение TCP — 65535 (FF:FF).
    - cmd[8:11] : Мкорость удаленной передачи, 0: неограниченно, 1-4294967295
    - cmd[12:15] : Мкорость локальной передачи, 0: неограниченно, 1-4294967295
- Сервер отвечает :
    - 01:00:00:00 - Если аутентификация сервера отключена, начинает передавать/получать данные. 
    - 02:00:00:00 и случайные байты (запрос) в диапазоне [4:15] - Если аутентификация включена и версия сервера btest < 6.43. 
    - 03:00:00:00 - Если версия сервера btest >= 6.43 и используется новый метод аутентификации, основанный на EC-SRP5.

#### Дополнительно
За основу взято средство [btest-opensource](https://github.com/samm-git/btest-opensource)



---
### [PoC на Python](./PoC.py), который реализует сбор информации
### [Форк lzr с bandwidth-test](https://github.com/SergoRoberto/lzr)


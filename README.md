# python_bivt
# Хаб-репозиторий курса (просто и по делу)

В этом репозитории — **правила и ссылки**, а также **задания для лабораторных**.  
Задания ищите тут: `./src/lab01/README.md`, `./src/lab02/README.md`, ...

---

## Что такое Git и система контроля версий (в двух словах)
- **Git** — инструмент для хранения истории кода (кто/что/когда изменил).
- Позволяет **возвращаться** к прошлым версиям, работать **вместе** и делать **ветки** для экспериментов.
- Репозиторий — это папка с историей (`.git`), которую можно хранить на GitHub и на своём компьютере.

## Что нужно сделать?
Для сдачи лабораторных работ Вам понадобится git-репозиторий. Чтобы его создать - необходимо создать аккаунт на github.com и добавить **ssh-ключ**.
### Как создать SSH-ключ (один раз)
**SSH-ключ** нужен, чтобы каждый раз не вводить логин/пароль при работе с GitHub.  
Процесс делится на 3 шага:

1. **Сгенерировать ключ** — команда `ssh-keygen` создаёт пару файлов (закрытый и открытый ключи).
2. **Найти ключ** — перейти в папку `.ssh` и вывести содержимое открытого ключа (`id_rsa.pub`).
3. **Добавить ключ в GitHub** — скопировать ключ и вставить в настройках GitHub.

**macOS / Linux**
Открываем терминал и вводим нужные команды
```bash
ssh-keygen -t rsa
# Нажмите Enter 3-4 раза
cat ~/.ssh/id_rsa.pub
```
![рис. 1 — генерация ключа ](./misc/img/general_material/macOS/ssh-keygen.png)

![](./misc/img/general_material/giphy.gif)

**Windows (PowerShell)**

В поисковой строке находим приложние cmd.exe 
![cmd](./misc/img/general_material/windows/cmd.jpg)

Введите команду
```powershell
ssh-keygen -t rsa
```
![ssh-keygen](./misc/img/general_material/windows/ssh-keygen_1.jpg)

Несколько раз нажмите **Enter**
![](./misc/img/general_material/windows/ssh-done.jpg)

Перейдите в папку с ключами и выведите содержимое, используя следующие команды:
```powershell
cd .ssh
type id_rsa.pub
```
**Обязетельно убедитесь, что находитесь в нужной дирекории** 
 ![Сменили директорию](./misc/img/general_material/windows/change-directory.jpg)

Вывели ключ
 ![Вывели ключик](./misc/img/general_material/windows/type-key.jpg)

### **Добавляем ключ на GitHub**

GitHub → Settings → **SSH and GPG keys** → **New SSH key** → вставьте содержимое `id_rsa.pub` → Save.  

Копируем содержимое ключа
![Пример ключа](./misc/img/general_material/macOS/highlighted.png)

Переходим в аккаунт
![](./misc/img/general_material/ssh_addition/account.png)

Заходим в настрйки
![](./misc/img/general_material/ssh_addition/settings.jpg)

![](./misc/img/general_material/e6UTws.gif)

Добавляем новый ключ
![](./misc/img/general_material/ssh_addition/new_ssh_button.png)

Вставляем содержимое `id_rsa.pub`
![](./misc/img/general_material/ssh_addition/new_ssh.jpg)

Жмем `Add SSH key`

### Что дальше? Создаем репозиторий.
GitHub → **Repository**
![](./misc/img/general_material/new_repo_repo.png)
**Repository → New**
![](./misc/img/general_material/new_repo_new.png)

**New Repository**→ `python_labs` → Public → Create.

![Новый репозиторий](./misc/img/lab01/new_repo.png)

### Как склонировать репозиторий на компьютер

1) На странице репозитория — кнопка **Code** → вкладка **SSH** → скопируйте URL.

![new_repo_code](./misc/img/general_material/repo_clone/new_repo_code.png)
![](./misc/img/general_material/repo_clone/ssh_key.png)

2) В терминале:
```bash
cd Desktop
git clone git@github.com:<owner>/<repo>.git
cd <repo>
```
#### Эти команды работают как на **Windows** так и на **MacOS**, покажу на примере **MacOS**:

Находясь в **корневой директории** (попасть в нее можно командой `cd` или `cd ..`), выполняем команду `cd Desktop` и проверяем, что мы оказались на рабочем столе
![change directory to desktop](./misc/img/general_material/repo_clone/cd_desktop.png)

![](./misc/img/general_material/vzhHSZ.gif)

Затем выполняем команду `git clone` и в качстве аргумента вставляем **ssh-url**, который мы скопировали на шаге 1.

![git clone](./misc/img/general_material/repo_clone/git-clone.png)
![git clone](./misc/img/general_material/repo_clone/git-clone-done.png)

После успешного выполнения команды открываем репозиторий в **visual studio code**
![done changes](./misc/img/general_material/repo_push/done_changes.png)
#### Индикаторы справа от названия директорий и файлов сигнализируют о том, что в репозиторий были внесены изменения и пора их опубликовать.

Открываем терминал. Можно как в **VS Code**, так и в том терминале что мы работали. Чтобы открыть терминал в **VS Code** используйте сочетание клавиш `ctrl + ~(ё)`
![Открыли терминал](./misc/img/general_material/repo_push/terminal_open.png)

![](./misc/img/general_material/subway-surfers-icegif-7.gif)

Добавляем файлы
![git add](./misc/img/general_material/repo_push/git-add.png)
Коммитим файлы
![git commit](./misc/img/general_material/repo_push/git-commit.png)
Публикуем файлы
![git push](./misc/img/general_material/repo_push/git-push.png)



# Где смотреть задания
- Для каждой лабораторной есть папка: `./src/lab01`, `./src/lab02`, ...  
- Внутри — **README.md** с заданием и мини-теорией.
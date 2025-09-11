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
## Как создать SSH-ключ (один раз)
Нужен, чтобы отправлять изменения в коде в GitHub-репозиторий без авторизации каждый раз.

**macOS / Linux**
```bash
ssh-keygen -t rsa
# Нажмите Enter 3 раза
cat ~/.ssh/id_rsa.pub
```
![рис. 1 — генерация ключа ](./misc/img/general_material/ssh-keygen.png)

**Windows (PowerShell)**
```powershell
ssh-keygen -t rsa
cd .ssh
type id_rsa.pub
```

**Добавьте ключ на GitHub**
GitHub → Settings → **SSH and GPG keys** → **New SSH key** → вставьте содержимое `id_rsa.pub` → Save.  

![Пример ключа](./misc/img/general_material/highlighted.png)
Копируем содержимое ключа

![](./misc/img/general_material/settings.jpg)
Заходим в настрйки

![](./misc/img/general_material/new_ssh.jpg)
Добавляем новый ключ

## Что дальше? Создаем репозиторий.
GitHub → **Repository**
![](./misc/img/general_material/new_repo_repo.png)
**Repository → New**
![](./misc/img/general_material/new_repo_new.png)

**New Repository**→ `python_labs` → Public → Create.

![Новый репозиторий](./misc/img/lab01/new_repo.png)

## Как склонировать репозиторий на компьютер

1) На странице репозитория — кнопка **Code** → вкладка **SSH** → скопируйте URL.

![new_repo_code](./misc/img/general_material/new_repo_code.png)

2) В терминале:
```bash
cd ~/Desktop
git clone git@github.com:<owner>/<repo>.git
cd <repo>
```
![](./misc/img/general_material/code-ssh.png)

![](./misc/img/lab01/%20clone_init_commit.png)

## Где смотреть задания
- Для каждой лабораторной есть папка: `./src/lab01`, `./src/lab02`, ...  
- Внутри — **README.md** с заданием и мини-теорией.
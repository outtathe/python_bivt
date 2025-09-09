# python_bivt
# Хаб-репозиторий курса (просто и по делу)

В этом репозитории — **правила и ссылки**, а также **задания для лабораторных**.  
Задания ищите тут: `./src/lab01/README.md`, `./src/lab02/README.md`, ...

---

## Что такое Git и система контроля версий (в двух словах)
- **Git** — инструмент для хранения истории кода (кто/что/когда изменил).
- Позволяет **возвращаться** к прошлым версиям, работать **вместе** и делать **ветки** для экспериментов.
- Репозиторий — это папка с историей (`.git`), которую можно хранить на GitHub и на своём компьютере.

## Как создать SSH-ключ (один раз)
Нужен, чтобы пушить на GitHub без ввода пароля каждый раз.

**macOS / Linux**
```bash
ssh-keygen -t rsa
# Нажмите Enter 3 раза
cat ~/.ssh/id_rsa.pub
```
![](./misc/img/ssh-keygen.jpg)

**Windows (PowerShell)**
```powershell
ssh-keygen -t rsa
type $env:USERPROFILE\.ssh\id_rsa.pub
```

**Добавьте ключ на GitHub**
GitHub → Settings → **SSH and GPG keys** → **New SSH key** → вставьте содержимое `id_rsa.pub` → Save.  

![](./misc/img/highlighted.jpg)
Копируем содержимое ключа

![](./misc/img/settings.jpg)
Заходим в настрйки

![](./misc/img/new_ssh.jpg)
Добавляем новый ключ

## Как склонировать репозиторий на компьютер
1) На странице репозитория — кнопка **Code** → вкладка **SSH** → скопируйте URL.  
2) В терминале:
```bash
cd ~/Desktop
git clone git@github.com:<owner>/<repo>.git
cd <repo>
```
![](./misc/img/code-ssh.jpg)

![](./misc/img/git-clone.jpg)

## Где смотреть задания
- Для каждой лабораторной есть папка: `./src/lab01`, `./src/lab02`, ...  
- Внутри — **README.md** с заданием и мини-теорией.
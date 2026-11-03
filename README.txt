ЛАБОРАТОРНАЯ РАБОТА №9
Запуск автоматизированных тестов в GitHub Actions

ЧТО УЖЕ ПОДГОТОВЛЕНО
В папке находятся:
- delivery.html — локальная форма расчета доставки (из ЛР №8);
- conftest.py — фикстура, открывающая форму перед каждым тестом;
- test_delivery_ui.py — все 12 тестов из ЛР №8;
- requirements.txt — зависимость pytest-playwright;
- .github/workflows/ui-tests.yml — автоматический запуск тестов в GitHub Actions;
- README.md — краткое описание проекта;
- .gitignore — исключает виртуальное окружение и временные результаты.

ВАЖНО
Для фактического запуска GitHub Actions проект необходимо загрузить в ваш GitHub-
репозиторий. Архив подготовлен локально; удаленный запуск и скриншоты Actions
можно получить только после загрузки в аккаунт GitHub. Не показывайте преподавателю
непроверенные/вымышленные скриншоты — откройте реальные результаты своего запуска.

1. ЧТО НУЖНО УСТАНОВИТЬ
- Python 3.11 или новее;
- Git (для отправки проекта через терминал) или доступ к GitHub в браузере.

2. ЛОКАЛЬНЫЙ ЗАПУСК В WINDOWS
Распакуйте архив. Откройте PowerShell именно в папке lab9_ci.

Создайте виртуальное окружение:
  py -m venv .venv

Установите зависимости:
  .venv\Scripts\python.exe -m pip install -r requirements.txt

Установите браузер Chromium для Playwright:
  .venv\Scripts\python.exe -m playwright install chromium

Откройте ПЕРВЫЙ PowerShell и запустите локальный сервер:
  .venv\Scripts\python.exe -m http.server 8000 --bind 127.0.0.1

Не закрывайте это окно. В браузере при желании откройте:
  http://127.0.0.1:8000/delivery.html

Откройте ВТОРОЙ PowerShell в той же папке и выполните:
  .venv\Scripts\python.exe -m pytest --collect-only -q

Должно обнаружиться 12 тестов. Затем полный запуск:
  .venv\Scripts\python.exe -m pytest -v --browser chromium --screenshot only-on-failure --tracing retain-on-failure --output test-results --junitxml=report.xml

Ожидаемый результат исправной версии: 12 passed.
Для успешного прогона скриншоты и trace могут не создаваться, поскольку они
сохраняются при падениях. XML-отчет report.xml создается.

3. ЗАГРУЗКА НА GITHUB
1) Войдите на https://github.com и создайте новый публичный или приватный репозиторий,
   например lab9-playwright-ci. Не добавляйте README или .gitignore автоматически,
   если загружаете уже подготовленные файлы проекта.
2) В папке проекта откройте PowerShell и выполните (замените URL на адрес своего репозитория):

  git init
  git add .
  git commit -m "Add Playwright UI tests and GitHub Actions CI"
  git branch -M main
  git remote add origin https://github.com/ВАШ_ЛОГИН/lab9-playwright-ci.git
  git push -u origin main

Если Git не установлен, можно загрузить файлы через веб-интерфейс GitHub.
Обязательно сохраните структуру .github/workflows/ui-tests.yml.

4. ПРОВЕРКА GITHUB ACTIONS
1) Откройте репозиторий на GitHub.
2) Перейдите во вкладку Actions.
3) Выберите workflow "Playwright UI tests".
4) Откройте последний запуск и job "ui-tests".
5) Убедитесь, что шаги Checkout, Set up Python, Show Python version,
   Install dependencies and browser, Start local application, Run UI tests
   и Upload test results выполнены.
6) В шаге Run UI tests найдите итог "12 passed"; общий статус должен быть Success.
7) Внизу страницы запуска найдите Artifacts и скачайте ui-test-results.
   В архиве проверьте report.xml. При падениях могут присутствовать материалы
   в test-results/. server.log — журнал локального HTTP-сервера.

Workflow запускается автоматически при push и pull_request, а также вручную
через workflow_dispatch (кнопка Run workflow, если доступна для ветки).

5. ПРОВЕРКА QUALITY GATE: НАМЕРЕННОЕ ПАДЕНИЕ ДВУХ ТЕСТОВ
Сначала убедитесь, что исправная версия сохранена (условие >= 10000).
Для демонстрации дефекта откройте delivery.html и найдите:
  const fee = value >= 10000 ? 0 :

Временно замените >= на >:
  const fee = value > 10000 ? 0 :

Сохраните и отправьте изменение:
  git add delivery.html
  git commit -m "Demonstrate boundary regression"
  git push

Откройте новый запуск в Actions. Ожидается 10 passed и 2 failed:
падают случаи №3 и №7 — сумма ровно 10000 для city и region.
Причина: при ошибочном условии > сумма 10000 больше не попадает в диапазон
бесплатной доставки, поэтому приложение начисляет плату, а тесты ожидают 0 ₸.
Job должен иметь статус Failure. Это правильная демонстрация quality gate:
CI блокирует изменение, нарушившее проверяемое поведение.

ОБЯЗАТЕЛЬНО восстановите правильное условие:
  const fee = value >= 10000 ? 0 :

Затем выполните:
  git add delivery.html
  git commit -m "Restore free delivery boundary"
  git push

В Actions дождитесь нового результата 12 passed / Success.

6. САМОСТОЯТЕЛЬНОЕ ЗАДАНИЕ ИЗ ЛР №9
- Шаг Show Python version уже добавлен в workflow; в Actions откройте его лог
  и покажите версию Python.
- Для pull request создайте ветку:
    git checkout -b readme-update
  внесите небольшое безопасное изменение в README.md, затем:
    git add README.md
    git commit -m "Update README"
    git push -u origin readme-update
  На GitHub нажмите Compare & pull request, затем Create pull request.
  Вкладка Actions должна показать запуск по pull_request. После проверки PR можно
  закрыть или выполнить merge по указанию преподавателя.
- server.log загружается в общий артефакт ui-test-results вместе с report.xml
  и test-results/.

7. ЧТО ПОКАЗАТЬ ПРЕПОДАВАТЕЛЮ
Подготовьте реальные скриншоты и покажите по порядку:

1) Папка проекта и структура файлов:
   delivery.html, conftest.py, test_delivery_ui.py, requirements.txt,
   .github/workflows/ui-tests.yml.
2) Содержимое workflow ui-tests.yml: события push, pull_request,
   workflow_dispatch; Python 3.11; установка Chromium; запуск сервера;
   pytest; загрузка артефактов через if: always().
3) Локальный запуск тестов: команда pytest и итог 12 passed.
4) GitHub → Actions → успешный запуск: зеленый Success, job ui-tests,
   шаг Show Python version и строка 12 passed.
5) Artifacts → ui-test-results: показать скачанный архив и report.xml.
6) Запуск с намеренным дефектом (замена >= на >): 10 passed, 2 failed,
   названия/ошибки тестов №3 и №7; статус job Failure.
7) Восстановление >=: новый запуск 12 passed и Success.
8) Pull request: страница PR и связанный успешный запуск workflow по событию
   pull_request.
9) Показать server.log, report.xml и, если они создались при падении,
   скриншоты и trace.zip из test-results/.

ЧЕМ ОТЛИЧАЮТСЯ МАТЕРИАЛЫ
- report.xml — структурированный JUnit XML: сколько тестов прошло/упало и
  сведения об ошибках; удобен для CI и отчетности.
- server.log — текстовый журнал работы локального HTTP-сервера (запросы,
  ошибки сервера). Он не описывает проверки pytest.
- screenshot — снимок состояния страницы в момент ошибки.
- trace.zip — трассировка Playwright: действия, состояние страницы и сведения
  для расследования сбоя.

8. КОНТРОЛЬНЫЕ ВОПРОСЫ (КРАТКИЕ ОТВЕТЫ)
1) Чем CI отличается от локального запуска тестов?
   Локально тесты запускает разработчик вручную на своем компьютере. CI запускает
   их автоматически на удаленном runner при push или pull_request.
2) Что такое workflow, job, step и runner?
   Workflow — YAML-сценарий автоматизации; job — группа шагов; step — отдельное
   действие или команда; runner — виртуальная машина, выполняющая job.
3) Зачем запускать по push и pull_request?
   Push проверяет отправленные изменения, pull_request проверяет изменения до
   их слияния в основную ветку.
4) Почему HTTP-сервер запускается на CI runner?
   Браузерные тесты обращаются к локальной странице по адресу 127.0.0.1:8000;
   на удаленном runner нужен свой экземпляр сервера.
5) Для чего if: always() при загрузке артефактов?
   Чтобы попытаться загрузить отчеты и диагностику даже если тестовый шаг завершился
   ошибкой. Сам job при этом остается failed.
6) Чем XML-отчет отличается от скриншота и трассировки?
   XML суммирует результаты тестов и ошибки; скриншот фиксирует внешний вид страницы;
   trace содержит последовательность действий и состояние браузера.
7) Почему >= на > приводит к двум отказам?
   Ровно 10000 перестает считаться порогом бесплатной доставки; падают два теста
   на этой границе — city и region.

9. ЕСЛИ ЧТО-ТО НЕ РАБОТАЕТ
- Connection refused: сервер не запущен или URL/порт не совпадает.
- Ошибка браузера: повторите playwright install chromium локально; в CI используется
  playwright install --with-deps chromium.
- Не найдено 12 тестов: проверьте имя test_delivery_ui.py и наличие всех тестов.
- Workflow не появляется: проверьте точный путь .github/workflows/ui-tests.yml
  и что файл отправлен в репозиторий.
- Не загружается артефакт: откройте лог шага Upload test results; он выполняется
  даже после падения тестов, но отсутствующие файлы могут быть пропущены.

УСПЕШНЫЙ ФИНАЛЬНЫЙ РЕЗУЛЬТАТ
Исправная версия delivery.html с условием >= 10000, 12 passed локально и в CI,
успешный запуск по pull_request, а также артефакт ui-test-results.

# Проєкт GenAI Sketch-to-Image

## Опис проєкту
Цей проєкт спрямований на використання генеративного штучного інтелекту (GenAI) для перетворення ручних ескізів у реалістичні зображення. Користувачі можуть малювати ескізи у веб-інтерфейсі, надсилати їх для обробки та отримувати детальний опис зображення і реалістичну версію свого ескізу. Проєкт демонструє використання сучасних інструментів ШІ для створення креативного контенту.

## Функціонал
- **Завантаження ескізів**: Веб-інтерфейс для створення та завантаження ескізів.
- **Опис зображення**: Автоматична генерація детальних описів зображень за допомогою OpenAI API.
- **Перетворення ескізів у зображення**: Трансформація ескізів у реалістичні зображення за допомогою WorqHat API.
- **Обробка зображень**: Ефективна обробка та збереження завантажених і згенерованих зображень.
- **Інтерактивний інтерфейс**: Зручний інтерфейс з миттєвим зворотним зв'язком.

## Технічний підхід
1. **Бекенд**:
   - **Фреймворк**: Flask для створення API та запуску застосунку.
   - **Обробка зображень**: Бібліотека PIL для обробки та комбінування зображень.
   - **API**:
     - OpenAI API для генерації детальних описів зображень.
     - WorqHat API для перетворення ескізів у реалістичні зображення.
2. **Фронтенд**:
   - **HTML/CSS/JavaScript**: Забезпечення адаптивного та інтерактивного веб-інтерфейсу.
   - **Інструмент для малювання**: Canvas для створення ескізів за допомогою бібліотеки DrawingTool.
3. **Сховище**:
   - Завантажені ескізи та згенеровані зображення зберігаються у структурованій директорії.
4. **Змінні середовища**:
   - Керування API-ключами через змінні середовища для безпеки.

## Інсталяція
### Вимоги
- Python 3.9 або новіша версія
- Pip

### Налаштування
1. Клонуйте репозиторій:
   ```bash
   git clone git@github.com:yuri-val/sketch-image.git
   cd sketch-image
   ```
2. Створіть віртуальне середовище та активуйте його:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows використовуйте venv\Scripts\activate
   ```
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
4. Налаштуйте змінні середовища для API-ключів:
   ```bash
   export SCG_OPENAI_API_KEY="<your_openai_api_key>"
   export WORQHAT_API_KEY="<your_worqhat_api_key>"
   ```
5. Запустіть застосунок:
   ```bash
   python app.py
   ```
6. Відкрийте застосунок у браузері за адресою `http://localhost:5000`.

## Metrics
### All Metrics

```python
from metrics.metrics_collector import MetricsCollector

uuid = "53ddf04b-1a7f-4894-90d6-79605244d5d5"
mc = MetricsCollector(uuid)

mc.analyze()

```

### CLIP Similarity

```python
from metrics.clip_similarity import CLIPSimilarity

uuid = "bbc9c3c7-6b71-4dbb-8739-f321306e908d"

or_im_path = f"storage/data/{uuid}/original.png"
gen_im_path = f"storage/data/{uuid}/generated.png"
description = open(f"storage/data/{uuid}/description.txt").read()

cs = CLIPSimilarity()
or_score = cs.compute_similarity(or_im_path, description)
gen_score = cs.compute_similarity(gen_im_path, description)

print(f'[ORIGINAL] CLIP Similarity score: {or_score}')
print(f'[GENERATED] CLIP Similarity score: {gen_score}')
 

```

### Object Detection Matching
```python
from metrics.object_detection_matching import ObjectDetectionMatching

uuid = "53ddf04b-1a7f-4894-90d6-79605244d5d5"

or_im_path = f"storage/data/{uuid}/original.png"
gen_im_path = f"storage/data/{uuid}/generated.png"
description = open(f"storage/data/{uuid}/description.txt").read()

object_matcher = ObjectDetectionMatching()

object_matcher.extract_objects_from_text(description)

or_object_match_score = object_matcher.compute_object_match_score(or_im_path, description)
gen_object_match_score = object_matcher.compute_object_match_score(gen_im_path, description)

print(f"[ORIGINAL] Object Detection Match Score: {or_object_match_score:.2f}%")
print(f"[GENERATED] Object Detection Match Score: {gen_object_match_score:.2f}%")

```


## Використання
1. Відкрийте веб-інтерфейс.
2. Намалюйте ескіз за допомогою інструменту для малювання або завантажте готовий ескіз.
3. Натисніть кнопку "Magic" для обробки ескізу.
4. Отримайте згенероване реалістичне зображення та його детальний опис.

## Виклики та їх вирішення
- **Виклик**: Обробка ескізів різної якості.
  - **Рішення**: Використано стійку передобробку зображень за допомогою PIL.
- **Виклик**: Забезпечення надійності API-відповідей.
  - **Рішення**: Додано обробку виключень та повторні запити.
- **Виклик**: Миттєвий зворотний зв'язок у користувацькому інтерфейсі.
  - **Рішення**: Реалізовано індикатор завантаження та динамічне оновлення контенту за допомогою JavaScript.

## Результати
- **Якість виводу**: Система генерує високоякісні реалістичні зображення та детальні описи.
- **Продуктивність**: Ефективний процесинг з низькою затримкою.
- **Користувацький досвід**: Інтуїтивно зрозумілий та привабливий інтерфейс.

## Майбутні покращення
- Додати підтримку пакетної обробки ескізів.
- Покращити генерацію описів за рахунок додаткового контексту або введення від користувача.
- Реалізувати автентифікацію користувачів для персоналізованого збереження зображень.
- Дослідити інтеграцію з іншими AI-інструментами для підвищення реалізму.

## Структура репозиторію
```
.
├── app.py               # Flask-застосунок
├── requirements.txt     # Залежності проєкту
├── service              # Сервіси бекенду
│   ├── image_describer.py
│   ├── image_processor.py
│   └── sketch_converter.py
├── static               # Фронтенд-ресурси
│   ├── index.html
│   ├── javascript
│   │   ├── api.js
│   │   └── dt-init.js
│   └── styles
│       └── styles.css
├── storage              # Завантажені та згенеровані зображення
│   ├── generated
│   └── uploads
└── templates            # HTML-шаблони (за потреби)
```

## Ліцензія
Цей проєкт ліцензовано під MIT License. Деталі дивіться у файлі LICENSE.

## Автори
- [Yuri V](https://github.com/yuri-val)

## Подяки
- [OpenAI](https://github.com/openai/openai-python) та [WorqHat](https://docs.worqhat.com/api-8951020) за їхні API
- Розробники [Flask](https://github.com/pallets/flask) і [PIL](https://github.com/python-pillow/Pillow)
- Бібліотека [DrawingTool](https://github.com/concord-consortium/drawing-tool) за підтримку інтерактивного полотна


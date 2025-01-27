# Проєкт GenAI Sketch-to-Image

## Опис проєкту
Цей проєкт спрямований на використання генеративного штучного інтелекту (GenAI) для перетворення ручних ескізів у реалістичні зображення. Користувачі можуть малювати ескізи у веб-інтерфейсі, надсилати їх для обробки та отримувати детальний опис зображення і реалістичну версію свого ескізу. Проєкт демонструє використання сучасних інструментів ШІ для створення креативного контенту.

## Функціонал
- **Завантаження ескізів**: Веб-інтерфейс для створення та завантаження ескізів
- **Опис зображення**: Автоматична генерація детальних описів зображень за допомогою WorqHat API
- **Перетворення ескізів у зображення**: Трансформація ескізів у реалістичні зображення
- **Обробка зображень**: Ефективна обробка та збереження завантажених і згенерованих зображень
- **Метрики оцінки**: Вбудовані метрики для оцінки якості генерації

## Технічний стек
1. **Бекенд**:
   - Flask для API та веб-серверу
   - PIL для обробки зображень
   - WorqHat API для генерації зображень та описів
   - AWS S3 для збереження файлів

2. **AI/ML компоненти**:
   - CLIP для обчислення схожості зображень
   - YOLO для детекції об'єктів
   - FID метрики для оцінки якості
   - SSIM для структурного порівняння зображень

3. **Фронтенд**:
   - HTML/CSS/JavaScript
   - Canvas для малювання
   - DrawingTool для інтерфейсу малювання

## Метрики оцінки
Проєкт включає наступні метрики для оцінки якості генерації:

1. **CLIP Similarity**:
   - Оцінює семантичну схожість між зображенням та описом
   - Використовує модель CLIP від OpenAI

2. **Object Detection Matching**:
   - Порівнює об'єкти, виявлені на зображенні, з описаними в тексті
   - Використовує YOLOv8 для детекції об'єктів

3. **FID (Fréchet Inception Distance)**:
   - Оцінює якість згенерованих зображень
   - Порівнює розподіли ознак оригінального та згенерованого зображень

4. **SSIM (Structural Similarity Index)**:
   - Оцінює структурну схожість між зображеннями
   - Враховує яскравість, контрастність і структуру

## Інсталяція
### Вимоги
- Python 3.9+
- pip
- віртуальне середовище Python

### Налаштування
1. Клонуйте репозиторій:
   ```bash
   git clone git@github.com:yuri-val/sketch-image.git
   cd sketch-image
   ```

2. Створіть віртуальне середовище:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

4. Налаштуйте змінні середовища:
   ```bash
   export WORQHAT_API_KEY="your_worqhat_api_key"
   export AWS_ACCESS_KEY_ID="your_aws_access_key"
   export AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
   ```

## Використання

### Веб-інтерфейс
1. Запустіть сервер:
   ```bash
   python app.py
   ```
2. Відкрийте браузер за адресою `http://localhost:5050`
3. Намалюйте або завантажте ескіз
4. Натисніть кнопку "Magic" для обробки

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
├── requirements.txt     # Основні залежності проєкту
├── requirements.metrics.txt # Залежності для метрик
├── service              # Сервіси бекенду
│   ├── file_handler.py
│   ├── image_describer.py
│   ├── image_processor.py
│   └── sketch_converter.py
├── metrics              # Модулі для обчислення метрик
│   ├── clip_similarity.py
│   ├── fid_metric.py
│   ├── metrics_collector.py
│   ├── object_detection_matching.py
│   └── ssim_metric.py
├── static               # Фронтенд-ресурси
│   ├── index.html
│   ├── javascript
│   │   ├── api.js
│   │   └── dt-init.js
│   └── styles
│       └── styles.css
├── storage              # Завантажені та згенеровані зображення
│   ├── data
│   ├── generated
│   └── uploads
└── templates            # HTML-шаблони (за потреби)
```
## Ліцензія
Цей проєкт ліцензовано під MIT License. Деталі дивіться у файлі LICENSE.

## Автори
- [Yuri V](https://github.com/yuri-val)

## Подяки
- [WorqHat](https://docs.worqhat.com/api-8951020) за їх API
- Розробники [Flask](https://github.com/pallets/flask) і [PIL](https://github.com/python-pillow/Pillow)
- Бібліотека [DrawingTool](https://github.com/concord-consortium/drawing-tool) за підтримку інтерактивного полотна

```python
from service.image_describer import ImageDescriber
from dotenv import load_dotenv

load_dotenv('.env')

id = ImageDescriber()
id.get_description("storage/data/5e3574a4-6e8d-462d-9cd2-1fd7d64fa849/original.png")

# ---

from service.sketch_converter import SketchConverter
from dotenv import load_dotenv

load_dotenv('.env')

sc = SketchConverter()
sc.convert_sketch("storage/data/02a42860-7f1b-44d7-bd4f-3d8c3044c724/original.png", 'two dogs')

```

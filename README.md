# PPR management system

БАГИ/недоработки:
- ТЕСТЫ!
- разобраться с размером изображений для подтверждающих фото (ресайз)
- добавить замечания в модель schedule
- добавить формирование отчета для инженера
- добавить возможность выбора дня/месяца/недели
- добавить отметки о том, что нужно распечтать акт/протокол
- не сохранять временные файлы актов/протоколов
- убрать атрибуты form-control из forms.py. Использовать кастомные виджеты для темплейтов (addclass).

ФИЧИ:
- API + telegram bot
- на главную страницу запилить дашборд
- user activity в админке
- запилить тему из шаблона (SB admin?)
- возможно, стоит загружать фотографии с главной страницы?
- настроить периодическое удаление дубликатов в истории (./manage.py clean_duplicate_history --auto), а также удаление устаревших записей
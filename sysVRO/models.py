from django.db import models
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', default='')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    SCALES = [('Отрядное', 'Отрядное'), ('Учебного заведения', 'Учебного заведения'),
              ('Региональное', 'Региональное'), ('Всероссийское', 'Всероссийское')]
    scale = models.CharField(max_length=20, choices=SCALES, default='Отрядное', verbose_name='Масштаб')
    FORMS = [('Офлайн', 'Офлайн'), ('Онлайн', 'Онлайн')]
    form = models.CharField(max_length=7, choices=FORMS, default='Офлайн', verbose_name='Форма проведения')
    kind = models.ManyToManyField('EventKind', blank=True, verbose_name='Тип мероприятия')
    beginning_date = models.DateField(db_index=True, verbose_name='Дата начала мероприятия')
    beginning_time = models.TimeField(null=True, blank=True, verbose_name='Время начала мероприятия')
    ending_date = models.DateField(null=True, blank=True, verbose_name='Дата конца мероприятия')
    photo = models.ImageField(null=True, blank=True, upload_to='event/img', verbose_name='Картинка мероприятия')
    color = models.ForeignKey('EventColor', null=True, blank=True, on_delete=models.PROTECT,
                              verbose_name='Цвет для градиента')
    content = models.TextField(default="", blank=True, verbose_name='Описание')
    place = models.CharField(max_length=50, blank=True, verbose_name='Место проведения', default='Волгоград')

    organizer = models.CharField(max_length=100, default="", blank=True, verbose_name='Организатор')
    contact = models.ForeignKey('Profile', null=True, blank=True, on_delete=models.PROTECT,
                                verbose_name='Контакт организатора', related_name='contact')
    admin = models.ManyToManyField('Profile', blank=True, verbose_name='Ответственные в системе')
    links = models.CharField(max_length=100, default="", blank=True, verbose_name='Ссылки на отчетные посты')

    # price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    # published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    # published2 = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'мероприятия'
        verbose_name = 'Мероприятие'
        ordering = ['-beginning_date']


class EventKind(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'типы мероприятий'
        verbose_name = 'Тип мероприятия'
        ordering = ['name']


class EventColor(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    rgb = models.CharField(max_length=7, verbose_name='#rrggbb')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'цвета мероприятий'
        verbose_name = 'Цвет мероприятия'
        ordering = ['name']


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=20, blank=True, null=True, verbose_name='Отчество')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name='Аватарка')
    institution = models.ForeignKey('Institution', null=True, blank=True, on_delete=models.PROTECT,
                                    verbose_name='Учебное заведение')
    link_vk = models.CharField(max_length=50, blank=True, verbose_name='Ссылка ВК', default='https://vk.com/')
    about = models.CharField(max_length=400, blank=True, verbose_name='О себе', default='')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Телефон', default='+7')
    membership_fee = models.BooleanField(default=False, verbose_name='Членский взнос оплачен')

    detachment = models.ForeignKey('Detachment', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Отряд')
    POSITIONS = [('', 'Без должности'), ('Комиссар', 'Комиссар'), ('Мастер-методист', 'Мастер-методист'),
                 ('Специалист', 'Специалист'), ('Командир', 'Командир')]
    position = models.CharField(max_length=20, blank=True, choices=POSITIONS, default='', verbose_name='Должность')

    @property
    def position_output(self):
        # Если должность в отряде то ЕЁ, инче если оплачен членский БОЕЦ, иначе КАНДИДАТ
        # return ''.join([self.detachment.name, ' Боец'])
        if self.position == '':
            if self.membership_fee:
                return 'Боец'
            else:
                return 'Кандидат'
        else:
            return self.position

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)

    class Meta:
        verbose_name_plural = 'профили'
        verbose_name = 'Профиль'


class Institution(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Полное название', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'учебные заведения'
        verbose_name = 'Учебное заведение'
        ordering = ['name']


class Mark(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, verbose_name='Мероприятие')
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Профиль')
    points = models.IntegerField(default=0, verbose_name='Количество баллов')
    about = models.CharField(max_length=200, blank=True, verbose_name='Описание выполненной работы', default='')
    organizer = models.BooleanField(default=False, verbose_name='Организатор')
    confirmed = models.BooleanField(default=False, verbose_name='Подтверждено')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        line = self.event.title + " " + self.profile.user.username
        return line

    class Meta:
        verbose_name_plural = 'оценки'
        verbose_name = 'Оценка'
        ordering = ['event']


class Detachment(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    # Уровень Линейный отряд, Штаб учебного заведения, Региональное отделение, (Направление)
    area = models.ForeignKey('Area', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Направление')
    institution = models.ForeignKey('Institution', null=True, blank=True, on_delete=models.PROTECT,
                                    verbose_name='Учебное заведение')
    flag = models.ImageField(upload_to='flags/%Y/%m/%d', blank=True, verbose_name='Флаг')
    emblem = models.ImageField(upload_to='emblems/%Y/%m/%d', blank=True, verbose_name='Эмблема')
    link_vk = models.CharField(max_length=50, blank=True, verbose_name='Ссылка ВК', default='https://vk.com/')
    about = models.CharField(max_length=400, blank=True, verbose_name='Об отряде', default='')

    commander = models.OneToOneField(Profile, related_name='commander', null=True, blank=True, on_delete=models.PROTECT,
                                     verbose_name='Командир')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'отряды'
        verbose_name = 'Отряд'


class Area(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    abbreviation = models.CharField(max_length=50, db_index=True, null=True, verbose_name='Аббревиатура')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'направления'
        verbose_name = 'Направление'
        ordering = ['name']

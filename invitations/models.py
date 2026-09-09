import uuid
from django.db import models


class Invitation(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Үйлөнүү той'),
        ('kyz_uzatuu', 'Кыз узатуу'),
        ('beshik', 'Бешик той'),
        ('jubilee', 'Юбилей / Мүчөл жаш'),
    ]

    slug = models.SlugField("Шилтеме (slug)", unique=True, help_text="Шилтеме үчүн уникалдуу сөз")
    event_type = models.CharField("Тойдун түрү", max_length=20, choices=EVENT_TYPES, default='wedding')

    groom_name = models.CharField("Күйөө баланын аты", max_length=50, blank=True, null=True, help_text="Мисалы: Байыш")
    bride_name = models.CharField("Келиндин аты", max_length=50, blank=True, null=True, help_text="Мисалы: Айдай")

    hosts_parents = models.CharField("Той ээлери (Ата-энеси)", max_length=150, help_text="Мисалы: Нүрканбек & Эльмира")
    invitation_text = models.TextField("Чакыруу тексти", blank=True, null=True)

    event_date = models.DateField("Тойдун датасы")
    event_time = models.TimeField("Башталуу убактысы", default="17:00")

    city = models.CharField("Шаар / Айыл", max_length=100, default="Бишкек шаары")
    restaurant_name = models.CharField("Ресторандын аты", max_length=100)
    map_link = models.URLField("2GIS / Яндекс Карта шилтемеси", blank=True, null=True)

    cover_image = models.ImageField("Башкы сүрөт", upload_to='covers/', blank=True, null=True)
    music = models.FileField("Музыка (MP3)", upload_to='music/', blank=True, null=True)

    phone_number = models.CharField("WhatsApp номер (RSVP үчүн)", max_length=20, help_text="Мисалы: 996700000000")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.groom_name and self.bride_name:
            return f"{self.groom_name} & {self.bride_name} - {self.event_date}"
        return f"{self.hosts_parents} - {self.event_date}"


class Guest(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField("Коноктун аты", max_length=100, help_text="Мисалы: Асан & Үсөн")
    token = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    is_attending = models.BooleanField("Келеби?", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.invitation}"
from django.db import models

# для перевода. gettext_lazy - метод который помечает текст для перевода
from django.utils.translation import gettext_lazy as _
# ограничить перечень форматов загружаемых файлов
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# модель для загрузки файлов
class Media(models.Model):
    class FileType(models.TextChoices):
        IMAGE = 'image', _('Image')
        VIDEO = 'video', _('Video')
        DOCUMENT = 'document', _('Document')
        GIF = 'gif', _("Gif")
        OTHER = 'other', _("Other")
    # поле "File" надо локализовать с помощью translation. "File" помечен для перевода
    # allowed_extensions - разрешенные разрешения для загрузки
    file = models.FileField(upload_to='only_medias/',
                            verbose_name=_("File"),
                            validators=[FileExtensionValidator(
                                allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp',
                                                    'mp4', 'mpeg4', 'avi', 'mov', 'mkv',
                                                    'pdf', 'doc', 'docx', 'gif']
                            )])
    # поле для выбора типа файла из класса class FileType
    file_type = models.CharField(max_length=10,
                                 verbose_name=_("File Type"),
                                 choices=FileType.choices)
    # метаданные
    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Media")

    # экземпляры как строковое представление в административной панели будет возвращать: Id и имена файлов.
    def __str__(self):
        return f"Id: {self.id}|Name: {self.file.name.split('/')[-1]}"

    # метод срабатывает при загрузке файлов. При сохранении экземпляров в базу данных
    def clean(self):
        # неразрешенный тип - ошибка. raise - вывод ошибки
        if self.file_type not in self.FileType.values:
            raise ValidationError(_("Invalid File Type"))
        # разрешенный тип IMAGE, но расширение не то -  raise. Расширение определяем через сплит имени по точке
        elif self.file_type == self.FileType.IMAGE:
            if self.file.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'svg', 'webp']:
                raise ValidationError(_("Invalid Image File"))
        elif self.file_type == self.FileType.VIDEO:
            if self.file.name.split('.')[-1] not in ['mp4', 'mpeg4', 'avi', 'mov', 'mkv']:
                raise ValidationError(_("Invalid Video File"))
        elif self.file_type == self.FileType.DOCUMENT:
            if self.file.name.split('.')[-1] not in ['pdf', 'doc', 'docx']:
                raise ValidationError(_("Invalid Document File"))

# модель для прочих изменяемых данных
class Settings(models.Model):
    main_phone_number = models.CharField(max_length=20, verbose_name=_("Main Phone Number"))
    title = models.TextField(verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    email = models.TextField(verbose_name=_("e-mail"), blank=True, null=True)
    # related_name - команда для вызова фотографии
    settings_page_image = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name=_("Settings Page Image"),
                                           related_name="settings_page_image")

    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return self.main_phone_number

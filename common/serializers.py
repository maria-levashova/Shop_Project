from rest_framework import serializers


class MediaURLSerializer(serializers.Serializer):
    def to_representation(self, media):
        if not media:
            return None
        try:
            return self.context["request"].build_absolute_uri(media.file.url)
        except Exception:
            return "http://testserver" + str(media.file.url)


# сериалайзер для модели Settings из common/models.py
# берем все поля модели, которые нужно сериализировать в JSON
class ConfigSerializer(serializers.Serializer):
    main_phone_number = serializers.CharField(max_length=20)
    title = serializers.CharField()
    description = serializers.CharField()
    email = serializers.CharField()
    settings_page_image = MediaURLSerializer()




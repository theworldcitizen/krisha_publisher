import os

CITIES = ["almaty", "nur-sultan", "shymkent", "akmolinskaja-oblast", "aktjubinskaja-oblast",
          "almatinskaja-oblast", "atyrauskaja-oblast", "vostochno-kazahstanskaja-oblast", "zhambylskaja-oblast",
          "zapadno-kazahstanskaja-oblast", "karagandinskaja-oblast", "kostanajskaja-oblast",
          "kyzylordinskaja-oblast", "mangistauskaja-oblast", "pavlodarskaja-oblast",
          "severo-kazahstanskaja-oblast", "juzhno-kazahstanskaja-oblast"]
CATEGORIES = ['doma', 'dachi', 'uchastkov', 'ofisa', 'pomeshhenija', 'zdanija', 'magazina', 'prombazy',
              'prochej-nedvizhimosti']


class RabbitMQ:
    RABBIT_MQ_HOST = os.environ.get('RABBIT_MQ_HOST', '192.168.88.147')
    RABBIT_MQ_PORT = os.environ.get('RABBIT_MQ_PORT', 5672)
    RABBIT_HTTP_PORT = os.environ.get('RABBIT_HTTP_PORT', 15672)
    RABBIT_MQ_PUBLISH_QUEUE = os.environ.get('RABBIT_MQ_PUBLISH_QUEUE', 'krisha_publish')
    RABBIT_MQ_LOGIN = os.environ.get('RABBIT_MQ_LOGIN', 'rabbit')
    RABBIT_MQ_PASSWORD = os.environ.get('RABBIT_MQ_PASSWORD', 'rabbit')
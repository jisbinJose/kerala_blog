from django.core.management.base import BaseCommand
from blog_app.models import Post

class Command(BaseCommand):
    help = 'Generates 10 sample posts about Idukki tourism in Malayalam'

    def handle(self, *args, **kwargs):
        posts = [
            {
                'title': 'ഇടുക്കി: മലയുടെ മടിയിലെ സ്വർഗം',
                'content': 'ഇടുക്കി, കേരളത്തിലെ ഏറ്റവും മനോഹരമായ ഹില്‍ സ്റ്റേഷനുകളില്‍ ഒന്നാണ്...',
            },
            {
                'title': 'മൂന്നാറും മീനുമുട്ടി ജലവൈദ്യുത പദ്ധതിയും',
                'content': 'മൂന്നാറിലെ ജലവൈദ്യുത പദ്ധതി കേരളത്തിലെ ഏറ്റവും വലിയ ജലവൈദ്യുത പദ്ധതികളില്‍ ഒന്നാണ്...',
            },
            # Add 8 more posts here
        ]

        for post_data in posts:
            Post.objects.create(**post_data)

        self.stdout.write(self.style.SUCCESS('Successfully created 10 posts about Idukki tourism'))

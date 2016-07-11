from .models import Profile

def save_avatar(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'facebook':
        profile.avatar = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
    elif backend.name == 'twitter':
        profile.avatar = response.get('profile_image_url', '').replace('_normal', '')
    elif backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
        profile.avatar = url
    # elif backend.name == 'linkedin-oauth2':
    #     fullname = profile.user.first_name + profile.user.last_name
    #     image_name = 'linked_avatar_%s.jpg' % fullname
    #     image_url = kwargs['response'].get['pictureUrl']
    #     image_stream = urlopen(image_url)
    #     profile.avatar.save(image_name, ContentFile(image_stream.read()),)

    profile.save()

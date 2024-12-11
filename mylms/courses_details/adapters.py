from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # You can add custom logic here to handle the email or any other data
        email = sociallogin.account.extra_data.get('email')
        if email:
            user.email = email
            user.save()
        return user

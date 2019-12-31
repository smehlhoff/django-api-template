from django.contrib.auth.tokens import PasswordResetTokenGenerator


def get_ip_address(request):
    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = request.META.get('REMOTE_ADDR')

    if http_x_forwarded_for:
        ip_address = http_x_forwarded_for.split(',')[-1].strip()
    elif remote_addr:
        ip_address = remote_addr
    else:
        ip_address = None

    return ip_address


def get_user_agent(request):
    http_user_agent = request.META.get('HTTP_USER_AGENT')

    if http_user_agent:
        user_agent = http_user_agent
    else:
        user_agent = None

    return user_agent


class EmailVerifyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(
            microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.primary_email.verified) + str(login_timestamp) + str(timestamp)


email_token_generator = EmailVerifyTokenGenerator()

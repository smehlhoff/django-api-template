from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class SignUpThrottle(AnonRateThrottle):
    scope = 'sustained'
    rate = '3/hour'


class SignInThrottle(AnonRateThrottle):
    scope = 'sustained'
    rate = '3/hour'


class ResetPasswordThrottle(AnonRateThrottle):
    scope = 'sustained'
    rate = '3/hour'


class VerifyEmailThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '3/hour'

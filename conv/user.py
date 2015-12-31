from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

# Ci dessous une copie de l'utilisateur "classique" de django
# avec nom prénom required
# et une date de dernière visite

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username = models.CharField(
        "Nom d'utilisateur/pseudo",
        max_length=254,
        unique=True,
        help_text=_('Required. 254 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_visit = models.DateField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    ###### custom methods

    def get_activity_at_ronde(self, ronde):
        """
        Returns what this user will do during the given ronde, either :
            ("", None)
            ("submitted_scenario", <Scenario whose author is self>)
            ("scenario", <Scenario the user participates to>)
            ("event", <Event the user participates to>)
        If the user is going to participate to several activities at the same time, raises ValidationError.
        """
        n = 0
        type = ""
        object = None
        for attr in ("submitted_scenario", "scenario", "event"):
            queryset = list(getattr(self, attr+"_set").filter(ronde=ronde))
            n += len(queryset)
            if n>1:
                raise ValidationError("L'utilisateur «{}» participe à plusieurs activités à la ronde {}".format(self, ronde))
            if len(queryset)==1:
                type = attr
                object = queryset[0]
        return type, object

    def is_busy_at_ronde(self, ronde):
        return bool(self.get_activity_at_ronde(ronde)[0])

# Un hack : 
def get_users(self, email):
    """Given an email, return matching user(s) who should receive a reset.
    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    active_users = get_user_model()._default_manager.filter(
        email__iexact=email, is_active=True)
    #return (u for u in active_users if u.has_usable_password())
    return active_users

import django.contrib.auth.forms
django.contrib.auth.forms.PasswordResetForm.get_users = get_users



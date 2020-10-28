from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumOneEightCharacters:
    """
    Validator which checks if password contains at least 8 characters
    """

    def __init__(self, contains_eight_char=True):
        self.contains_eight_char = contains_eight_char

    def validate(self, password, user=None):
        self.contains_eight_char = len(password)

        if self.contains_eight_char < 8:

            raise ValidationError(
                _("Le mot de passe doit contenir au moins 8 caractères."),
                code='password_too_short',
                params={'contains_eight_char': self.contains_eight_char},
            )

    def get_help_text(self):
        return _(
            "Le mot de passe doit contenir au moins 8 caractères."
            % {'contains_eight_char': self.contains_eight_char}
        )


class MinimumOneDigitValidator:
    """
    Validator which checks if password contains at least one number
    """

    def __init__(self, contains_digit=True):
        self.contains_digit = contains_digit

    def validate(self, password, user=None):
        self.contains_digit = any(map(str.isdigit, password))

        if not self.contains_digit:

            raise ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre."),
                code='password_without_digit',
                params={'contains_digit': self.contains_digit},
            )

    def get_help_text(self):
        return _(
            "Le mot de passe doit contenir au moins un chiffre."
            % {'contains_digit': self.contains_digit}
        )


class ContainOneLowerCharacter:
    """
    Validator which checks if password contains at least one lowercase character
    """

    def __init__(self, contains_lower=False):
        self.contains_lower = contains_lower

    def validate(self, password, user=None):
        self.contains_lower = any(map(str.islower, password))

        if not self.contains_lower:

            raise ValidationError(
                _("Le mot de passe doit contenir au moins un catactère en minuscule."),
                code='password_without_lower',
                params={'contains_lower': self.contains_lower},
            )

    def get_help_text(self):
        return _(
            "Le mot de passe doit contenir au moins un catactère en minuscule."
            % {'contains_lower': self.contains_lower}
        )


class ContainOneUpperCharacter:
    """
    Validator which checks if password contains at least one uppercase character
    """

    def __init__(self, contains_upper=False):
        self.contains_upper = contains_upper

    def validate(self, password, user=None):
        self.contains_upper = any(map(str.isupper, password))

        if not self.contains_upper:

            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère en majuscule."),
                code='password_without_upper',
                params={'contains_upper': self.contains_upper},
            )

    def get_help_text(self):
        return _(
            "Le mot de passe doit contenir au moins un caractère en majuscule."
            % {'contains_upper': self.contains_upper}
        )


class ContainSpecialCharacter:
    """
    Validator which checks if password contains at least one special character
    """

    def __init__(self, contains_special=False):
        self.contains_special = contains_special

    def validate(self, password, user=None):
        self.contains_special = any(not c.isalnum() for c in password)
        print(self.contains_special)

        if not self.contains_special:
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un catactère spécial."),
                code='password_without_specialchar',
                params={'contains_special': self.contains_special},
            )

    def get_help_text(self):
        return _(
            "Le mot de passe doit contenir au moins un catactère spécial."
            % {'contains_special': self.contains_special}
        )

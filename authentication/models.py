from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.contrib.auth import get_user_model  # Використовуємо get_user_model для уникнення прямого імпорту

# Ролі користувачів
ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)

# Менеджер для CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)  # За замовчуванням активний
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

# Модель CustomUser
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=True, default="")
    last_name = models.CharField(max_length=20, blank=True, default="")
    middle_name = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    # Групи та дозволи
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )

    # Поля для авторизації
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Прив'язка менеджера
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_name()})"

    def __repr__(self):
        return f"{CustomUser.__name__}(id={self.id})"

    # Методи для прав доступу
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Статичні методи
    @staticmethod
    def get_by_id(user_id):
        return CustomUser.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def delete_by_id(user_id):
        user_to_delete = CustomUser.objects.filter(id=user_id).first()
        if user_to_delete:
            user_to_delete.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name="", middle_name="", last_name=""):
        if not email or not password:
            raise ValueError("Email and password are required")
        if len(first_name) <= 20 and len(middle_name) <= 20 and len(last_name) <= 20 and len(email) <= 100 and '@' in email and not CustomUser.objects.filter(email=email).exists():
            custom_user = CustomUser(
                email=email,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name
            )
            custom_user.set_password(password)
            custom_user.save()
            return custom_user
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active,
        }

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if first_name and len(first_name) <= 20:
            self.first_name = first_name
        if last_name and len(last_name) <= 20:
            self.last_name = last_name
        if middle_name and len(middle_name) <= 20:
            self.middle_name = middle_name
        if password:
            self.set_password(password)
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role, 'Unknown')

# Модель Order
class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    book = models.ForeignKey(
        'book.Book', 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.email} for {self.book}"

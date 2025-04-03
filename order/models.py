from django.db import models, DataError
from authentication.models import CustomUser
from book.models import Book

class Order(models.Model):
    """
    This class represents an Order.
    Attributes:
    -----------
    param book: foreign key Book
    type book: ForeignKey
    param user: foreign key CustomUser
    type user: ForeignKey
    param created_at: Describes the date when the order was created. Can't be changed.
    type created_at: int (timestamp)
    param end_at: Describes the actual return date of the book. (`None` if not returned)
    type end_at: int (timestamp)
    param plated_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
    type plated_end_at: int (timestamp)
    """
    #book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None)

    def __str__(self):
        """
        Magic method is redefined to show all information about the Order.
        """
        if self.end_at is None:
            return f"\'id\': {self.pk}, \'user\': CustomUser(id={self.user.pk}), \'book\': Book(id={self.book.pk}), \'created_at\': \'{self.created_at}\', \'end_at\': {self.end_at}, \'plated_end_at\': \'{self.plated_end_at}\'"
        else:
            return f"\'id\': {self.pk}, \'user\': CustomUser(id={self.user.pk}), \'book\': Book(id={self.book.pk}), \'created_at\': \'{self.created_at}\', \'end_at\': \'{self.end_at}\', \'plated_end_at\': \'{self.plated_end_at}\'"

    def __repr__(self):
        """
        Magic method is redefined to show class and id of the Order object.
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        :return: order id, book id, user id, order created_at, order end_at, order plated_end_at
        :Example:
        {
           'id': 8,
           'book': 8,
           'user': 8,
           'created_at': 'timestamp',
           'end_at': 'timestamp',
           'plated_end_at': 'timestamp',
        }
        """
        return {
            'id': self.pk,
            'book': self.book.pk,
            'user': self.user.pk,
            'created_at': self.created_at,
            'end_at': self.end_at,
            'plated_end_at': self.plated_end_at
        }

    @staticmethod
    def create(user, book, plated_end_at):
        orders = Order.objects.all()
        books = set()
        for order in orders:
            if not order.end_at:
                books.add(order.book.id)
        if book.id in books and book.count == 1:
            return None
        try:
            order = Order(user=user, book=book, plated_end_at=plated_end_at)
            order.save()
            return order
        except (ValueError, DataError):
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None).values()

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return True
        except Order.DoesNotExist:
            return False

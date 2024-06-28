from django.db import models


class IssuedTickers(models.Model):
    id_issued_ticker = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=6)

    REQUIRED_FIELDS = ['ticker']

    class Meta:
        db_table = 'tb_issued_ticker'

    def __str__(self):
        return self.ticker

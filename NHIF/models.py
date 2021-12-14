from django.db import models


# Create your models here.
class Claims(models.Model):
    def __str__(self):
        return "%d" % self.id

    facility_hfr_code = models.CharField(max_length=255)
    claimed_amount = models.DecimalField(max_digits=20, decimal_places=2)
    period = models.CharField(max_length=255)
    date = models.DateField()
    computed_amount = models.DecimalField(max_digits=20, decimal_places=2)
    accepted_amount = models.DecimalField(max_digits=20, decimal_places=2)
    loan_deductions = models.DecimalField(max_digits=20, decimal_places=2)
    other_deductions = models.DecimalField(max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        db_table = "Claims"
        verbose_name_plural = "Claims"
from django.db import models


class Url(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200, unique=True)
    last_scraped = models.DateTimeField(auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'URLs'
        verbose_name_plural = 'URLs'


class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'States'
        verbose_name_plural = 'States'


class FranchiseType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Franchise Types'
        verbose_name_plural = 'Franchise Types'


class Franchise(models.Model):
    name = models.CharField(max_length=50)
    minimum_investiment = models.FloatField()
    min_return_month = models.PositiveSmallIntegerField()
    max_return_month = models.PositiveSmallIntegerField()

    state = models.ForeignKey(State, on_delete=models.CASCADE)
    ftype = models.ForeignKey(FranchiseType, on_delete=models.CASCADE)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, null=True)

    active_unities = models.PositiveIntegerField(default=0)
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Franchises'
        verbose_name_plural = 'Franchises'


class Tax(models.Model):
    calculus_base = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return self.calculus_base

    def __repr__(self):
        return self.calculus_base

    def __unicode__(self):
        return self.calculus_base

    class Meta:
        verbose_name = 'Taxes'
        verbose_name_plural = 'Taxes'


class Quiosque(models.Model):
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    installation_capital = models.FloatField()
    franchising_tax = models.FloatField()
    total_investiment = models.FloatField()

    investiment_return_month_min = models.PositiveSmallIntegerField()
    investiment_return_month_max = models.PositiveSmallIntegerField()

    state = models.ForeignKey(State, on_delete=models.CASCADE)

    area_min = models.PositiveSmallIntegerField()
    area_max = models.PositiveSmallIntegerField()

    employees_min = models.PositiveSmallIntegerField()
    employees_max = models.PositiveSmallIntegerField()

    publicity_tax = models.ForeignKey(Tax, on_delete=models.CASCADE)

    # royalties_tax = models.ForeignKey(Tax, on_delete=models.CASCADE)

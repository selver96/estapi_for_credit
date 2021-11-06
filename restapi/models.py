from django.db import models


class Programm(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    min_credit = models.IntegerField(verbose_name="Минимальный Кредит")
    max_credit = models.IntegerField(verbose_name="Максимальный кредит")
    min_age = models.IntegerField(verbose_name="Минимальный возрост")
    max_age = models.IntegerField(verbose_name="Максимальный возрост")

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"


class Borrower(models.Model):
    uin = models.CharField(max_length=12, unique=True, verbose_name="ИИН")
    birthday = models.DateField(verbose_name="Дата Рождение")

    def __str__(self) -> str:
        return str(self.uin)

    class Meta:
        verbose_name = "Заимщик"
        verbose_name_plural = "Заимщики"


class Application(models.Model):
    amount = models.IntegerField(verbose_name="Сумма")
    status = models.CharField(max_length=50, verbose_name="Статус")
    rejection_reason = models.CharField(max_length=150, null=True, verbose_name="Причина отказа")
    programm = models.ForeignKey(Programm, on_delete=models.SET_NULL, null=True, verbose_name="Программы")
    borrower = models.ForeignKey(Borrower, on_delete=models.SET_NULL, null=True, verbose_name="Заимщики")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class BlackList(models.Model):
    uin = models.CharField(max_length=12, unique=True, verbose_name="ИИН")

    class Meta:
        verbose_name = "Чёрный список"
        verbose_name_plural = "Чёрный список"
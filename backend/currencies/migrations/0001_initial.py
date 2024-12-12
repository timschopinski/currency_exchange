# Generated by Django 5.0 on 2024-12-12 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticker", models.CharField(max_length=3, unique=True)),
            ],
            options={
                "verbose_name_plural": "Currencies",
            },
        ),
        migrations.CreateModel(
            name="CurrencyPair",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "base_currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="base_currency_pairs",
                        to="currencies.currency",
                    ),
                ),
                (
                    "quote_currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quote_currency_pairs",
                        to="currencies.currency",
                    ),
                ),
            ],
            options={
                "unique_together": {("base_currency", "quote_currency")},
            },
        ),
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exchange_rate", models.DecimalField(decimal_places=4, max_digits=10)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "currency_pair",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_rates",
                        to="currencies.currencypair",
                    ),
                ),
            ],
            options={
                "verbose_name": "Exchange Rate",
                "verbose_name_plural": "Exchange Rates",
                "ordering": ["-timestamp"],
            },
        ),
    ]

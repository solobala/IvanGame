# Generated by Django 4.1.3 on 2022-12-15 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0034_race_fov_race_rov_alter_action_fov_alter_action_rov_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="person", name="person_name",),
        migrations.RemoveField(model_name="race", name="race_description",),
        migrations.AddField(
            model_name="owner",
            name="owner_img",
            field=models.ImageField(default="media/python.png", upload_to=""),
        ),
        migrations.AddField(
            model_name="person",
            name="person_img",
            field=models.ImageField(default="media/python.png", upload_to=""),
        ),
        migrations.AlterField(
            model_name="race",
            name="race_name",
            field=models.CharField(
                choices=[
                    ("0", "Эльф"),
                    ("1", "Ангел"),
                    ("2", "Феникс"),
                    ("3", "Дриада"),
                    ("4", "Демон"),
                    ("5", "Вампир"),
                    ("6", "Дроу"),
                    ("7", "Тень"),
                    ("8", "Арахнид"),
                    ("9", "Нежить"),
                    ("10", "Дракон"),
                    ("11", "Драконейт"),
                    ("12", "Оборотень"),
                    ("13", "Человек"),
                    ("14", "Гном"),
                    ("15", "Русал"),
                    ("16", "Зверин"),
                    ("17", "Звероподобное"),
                    ("18", "Змеелюд"),
                    ("19", "Метаморф"),
                    ("20", "Атлант"),
                    ("21", "Гоблин"),
                    ("22", "Орк"),
                    ("23", "прочие"),
                ],
                default="13",
                max_length=20,
            ),
        ),
    ]
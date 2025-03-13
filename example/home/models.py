from django.db import models

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from modelcluster.fields import ParentalKey


class FormField(AbstractFormField):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="form_fields")
    placeholder = models.CharField(
        max_length=255, blank=True, help_text="Texte de placeholder pour ce champ"
    )

    panels = AbstractFormField.panels + [
        FieldPanel("placeholder"),
    ]


class PlaceholderFormBuilder(FormBuilder):
    @property
    def formfields(self):
        # Récupérer les champs générés par le FormBuilder standard
        formfields = super().formfields

        # Types de champs textuels
        text_field_types = {
            "singleline",
            "multiline",
            "email",
            "number",
            "url",
            "date",
            "datetime",
        }

        # Modifier chaque champ textuel pour ajouter un placeholder
        for field in self.fields:
            if hasattr(field, "placeholder") and field.placeholder:
                field_name = field.clean_name or field.get_field_clean_name()

                # Vérifier si le champ est textuel avant d'ajouter le placeholder
                if field.field_type in text_field_types and field_name in formfields:
                    formfields[field_name].widget.attrs.update(
                        {"placeholder": field.placeholder}
                    )

        return formfields


class HomePage(AbstractEmailForm):
    form_builder = PlaceholderFormBuilder

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address"),
                        FieldPanel("to_address"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

from django import forms
from wagtail.core import blocks


class InteractiveChannelChooserBlock(blocks.ChooserBlock):
    from .models import InteractiveChannel

    target_model = InteractiveChannel
    widget = forms.Select


class CrankyUncleButtonBlock(blocks.StructBlock):
    subject = blocks.CharBlock()
    button_text = blocks.CharBlock()
    trigger_string = blocks.CharBlock()
    cranky_uncle_channel = InteractiveChannelChooserBlock()

    class Meta:
        icon = 'tag'
        # template = ''

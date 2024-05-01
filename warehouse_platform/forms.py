from django import forms
from django.forms import modelformset_factory
from .models import Item, ItemImage
from django.forms import ClearableFileInput

class ItemForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # Allows multiple files to be selected
        required=False,  # Set to False if not required
        help_text='Select multiple images for your listing.'
    )
    
    class Meta:
        model = Item
        fields = ['name', 'thumbnail', 'description', 'price', 'warehouse_type', 'area', 'camera_monitoring', 'contract_type', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].required = False  # Make thumbnail not required if you prefer


# If you're using a separate model for images
ItemImageFormSet = modelformset_factory(
    ItemImage,
    fields=('image', ),  # Explicitly specify which fields to include in the formset
    extra=1,  # Start with 1 empty form
    min_num=1,  # Require at least one image to be uploaded
    validate_min=True,  # Enable minimum number validation
    max_num=20,  # Set a reasonable max number, adjust according to your needs
    validate_max=True  # Enable maximum number validation
)

from django import forms
from .models import Item


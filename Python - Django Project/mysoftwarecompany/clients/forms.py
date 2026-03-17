from django import forms
from .models import Company, Employee

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 100, required = True)
    email = forms.EmailField(max_length = 100, required = True)
    message = forms.CharField(widget = forms.Textarea, required = True)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long")
        return name
    # def clean_name(self):
    #     email = self.cleaned_data.get("email")
    #     if len(email) < 2:
    #         raise forms.ValidationError("Name must be at least 2 characters long")
    #     return email
    def clean_method(self):
        message = self.cleaned_data.get("message")
        if len(message) < 50:
            raise forms.ValidationError("Message must be at least 50 characters long")
        return message
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if (len(name) < 3):
            raise forms.ValidationError("A company name must be at least 3 characters")
        return name
    def clean(self):
        cleaned_data= super().clean()
        name = self.cleaned_data.get('name','')
        description = self.cleaned_data.get('description', '')
        forbidden_words = ['spam', 'scam', 'fake']
        for word in forbidden_words:
            if word in description.lower() or word in name.lower():
                raise forms.ValidationError(f"The company caontains a forbidden word: {word}")
        return cleaned_data
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'role']
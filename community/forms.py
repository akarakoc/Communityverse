from django.contrib.auth import authenticate, get_user_model
from django import forms
from community.models import Primitives

class UsersLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput,)
    def __init__(self, *args, **kwargs):
        super(UsersLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name":"username"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name":"password"})
    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError("This user does not exists")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("User is no longer active")
        return super(UsersLoginForm, self).clean(*args, **keyargs)
 

User = get_user_model()

class UsersRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
                "username",
                "email",
                "confirm_email",
                "password",
                ]
    username = forms.CharField()
    email = forms.EmailField(label = "Email")
    confirm_email = forms.EmailField(label = "Confirm Email")
    password = forms.CharField(widget = forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(UsersRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name":"username"})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            "name":"email"})
        self.fields['confirm_email'].widget.attrs.update({
            'class': 'form-control',
            "name":"confirm_email"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name":"password"})
    def clean(self, *args, **keyargs):
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email != confirm_email:
            raise forms.ValidationError("Email must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email is already registered")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("User with this username already registered")
		#you can add more validations for password
        if len(password) < 8:
            raise forms.ValidationError("Password must be greater than 8 characters")
        return super(UsersRegisterForm, self).clean(*args, **keyargs)
 


class AddCommunity(forms.Form):
    Community_Name = forms.CharField()
    Community_Description = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}))
    Community_Tags = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}))
    Community_Image = forms.ImageField()
    Private_Community = forms.BooleanField(initial=False, required=False)
    def __init__(self, *args, **kwargs):
        super(AddCommunity, self).__init__(*args, **kwargs)
        self.fields['Community_Name'].label = "Community Name"
        self.fields['Community_Name'].widget.attrs.update({
            'class': 'form-control',
            "name":"Community Name"})
        self.fields['Community_Description'].label = "Community Description"
        self.fields['Community_Description'].widget.attrs.update({
            'class': 'form-control',
            "name":"Community Description"})
        self.fields['Community_Tags'].label = "Community Tags"
        self.fields['Community_Tags'].widget.attrs.update({
            'class': 'form-control',
            "name":"Community Tags"})
    def clean(self, *args, **keyargs):
        Community_Name = self.cleaned_data.get("Community Name")
        Community_Description = self.cleaned_data.get("Community Description")
        Community_Tags = self.cleaned_data.get("Community Tags")
        Community_Image = self.cleaned_data.get("Community Image")
        return super(AddCommunity, self).clean(*args, **keyargs) 
		

class AddDatatype(forms.Form):
    Datatype_Name = forms.CharField()
    Datatype_Tags = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}))
    Datatype_Image = forms.ImageField()
    def __init__(self, *args, **kwargs):
        super(AddDatatype, self).__init__(*args, **kwargs)
        self.fields['Datatype_Name'].label = "Datatype Name"
        self.fields['Datatype_Name'].widget.attrs.update({
            'class': 'form-control',
            "name":"Datatype Name"})
        self.fields['Datatype_Tags'].label = "Datatype Tags"
        self.fields['Datatype_Tags'].widget.attrs.update({
            'class': 'form-control',
            "name":"Datatype Tags"})
    def clean(self, *args, **keyargs):
        Datatype_Name = self.cleaned_data.get("Datatype Name")
        Datatype_Tags = self.cleaned_data.get("Datatype Tags")
        Datatype_Image = self.cleaned_data.get("Datatype Image")
        return super(AddDatatype, self).clean(*args, **keyargs)


class AddTextEntryEnum(forms.Form):
    name = forms.CharField(label='')
    Types = forms.ModelChoiceField(queryset=Primitives.objects.filter(name="Enumeration").order_by('name'),label='',to_field_name="name")
    Required = forms.BooleanField(initial=False, required=False, label='')
    ShowPage = forms.BooleanField(initial=False, required=False, label='')
    Enum = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(AddTextEntryEnum, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Types'].widget.attrs.update({'class': 'form-control'})
        self.fields['Enum'].widget.attrs.update({'class': 'form-control'})

class AddTextEntry(forms.Form):
    name = forms.CharField(label='')
    Types = forms.ModelChoiceField(queryset=Primitives.objects.all().exclude(name="Enumeration").order_by('name'),label='',to_field_name="name")
    Required = forms.BooleanField(initial=False, required=False, label='')
    ShowPage = forms.BooleanField(initial=False, required=False, label='')
    def __init__(self, *args, **kwargs):
        super(AddTextEntry, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['Types'].widget.attrs.update({'class': 'form-control'})
		
class SendPrimitives(forms.Form):
    Types = forms.ModelChoiceField(queryset=Primitives.objects.all().order_by('name'),label='')	
    def __init__(self, *args, **kwargs):
        super(SendPrimitives, self).__init__(*args, **kwargs)
        self.fields['Types'].widget.attrs.update({'class': 'form-control'})
		
class AddTextPost(forms.Form):
    TextEntry = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(AddTextPost, self).__init__(*args, **kwargs)
        self.fields['TextEntry'].widget.attrs.update({'class': 'form-control'})
		
		
class AddTextAreaPost(forms.Form):
    TextAreaEntry = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}),label='')
    def __init__(self, *args, **kwargs):
        super(AddTextAreaPost, self).__init__(*args, **kwargs)
        self.fields['TextAreaEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddImagePost(forms.Form):
    ImageEntry = forms.ImageField(label='')
    def __init__(self, *args, **kwargs):
        super(AddImagePost, self).__init__(*args, **kwargs)		
	
class AddAudioPost(forms.Form):
    AudioEntry = forms.FileField(label='')
    def __init__(self, *args, **kwargs):
        super(AddAudioPost, self).__init__(*args, **kwargs)
	
class AddVideoPost(forms.Form):
    VideoEntry = forms.FileField(label='')
    def __init__(self, *args, **kwargs):
        super(AddVideoPost, self).__init__(*args, **kwargs)
	
class AddBooleanPost(forms.Form):
    BooleanEntry = forms.BooleanField(initial=False, required=False,label='')
    def __init__(self, *args, **kwargs):
        super(AddBooleanPost, self).__init__(*args, **kwargs)
        self.fields['BooleanEntry'].widget.attrs.update({'class': 'form-control d-flex justify-content-between'})
	
class AddEmailPost(forms.Form):
    EmailEntry = forms.EmailField(label='')
    def __init__(self, *args, **kwargs):
        super(AddEmailPost, self).__init__(*args, **kwargs)
        self.fields['EmailEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddIpAddressPost(forms.Form):
    IpAddressEntry = forms.GenericIPAddressField(label='')
    def __init__(self, *args, **kwargs):
        super(AddIpAddressPost, self).__init__(*args, **kwargs)
        self.fields['IpAddressEntry'].widget.attrs.update({'class': 'form-control'})
		
class AddUrlPost(forms.Form):
    UrlEntry = forms.URLField(label='')
    def __init__(self, *args, **kwargs):
        super(AddUrlPost, self).__init__(*args, **kwargs)
        self.fields['UrlEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddDatePost(forms.Form):
    DateEntry = forms.DateField(label='')
    def __init__(self, *args, **kwargs):
        super(AddDatePost, self).__init__(*args, **kwargs)
        self.fields['DateEntry'].widget.attrs.update({'class': 'form-control','type': 'date'})
	
class AddTimePost(forms.Form):
    TimeEntry = forms.TimeField(label='')
    def __init__(self, *args, **kwargs):
        super(AddTimePost, self).__init__(*args, **kwargs)
        self.fields['TimeEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddDateTimePost(forms.Form):
    DateTimeEntry = forms.DateTimeField(label='')
    def __init__(self, *args, **kwargs):
        super(AddDateTimePost, self).__init__(*args, **kwargs)
        self.fields['DateTimeEntry'].widget.attrs.update({'class': 'form-control','type': 'datetime-local'})
	
class AddIntegerPost(forms.Form):
    IntegerEntry = forms.IntegerField(label='')
    def __init__(self, *args, **kwargs):
        super(AddIntegerPost, self).__init__(*args, **kwargs)
        self.fields['IntegerEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddDecimalPost(forms.Form):
    DecimalEntry = forms.DecimalField(label='')
    def __init__(self, *args, **kwargs):
        super(AddDecimalPost, self).__init__(*args, **kwargs)
        self.fields['DecimalEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddFloatPost(forms.Form):
    FloatEntry = forms.FloatField(label='')
    def __init__(self, *args, **kwargs):
        super(AddFloatPost, self).__init__(*args, **kwargs)
        self.fields['FloatEntry'].widget.attrs.update({'class': 'form-control'})
	
class AddEnumaratedPost(forms.Form):	
    def __init__(self, *args, **kwargs):
        enum = kwargs.pop('en')
        name = kwargs.pop('nm')
        super(AddEnumaratedPost, self).__init__(*args, **kwargs)
        self.fields['EnumaratedEntry'] = forms.ChoiceField(choices=tuple(enumerate(enum)),label='')
        self.fields['EnumaratedEntry'].widget.attrs.update({'class': 'form-control'})
        contextName={}
        contextName['name']=name
        cnName = contextName.get(name,name)
        super(AddEnumaratedPost, self).add_prefix(cnName)
        
class AddLocationPost(forms.Form):
    LocationEntry = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(AddLocationPost, self).__init__(*args, **kwargs)
        self.fields['LocationEntry'].widget.attrs.update({'class': 'form-control'})

class AddTagPost(forms.Form):
    TagEntry = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}),label='')
    def __init__(self, *args, **kwargs):
        super(AddTagPost, self).__init__(*args, **kwargs)
        self.fields['TagEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['TagEntry'].widget.attrs.update({'data-role': 'tagsinput'})


#######################################################################################################		
###################################SEARCH FORMS########################################################
#######################################################################################################

class AddTextSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    TextEntry = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(AddTextSearch, self).__init__(*args, **kwargs)
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})		
        self.fields['TextEntry'].widget.attrs.update({'class': 'form-control'})		
		
class AddTextAreaSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    TextAreaEntry = forms.CharField(widget=forms.Textarea(attrs={'width':"50%", 'cols' : "50", 'rows': "2",}),label='')
    def __init__(self, *args, **kwargs):
        super(AddTextAreaSearch, self).__init__(*args, **kwargs)
        self.fields['TextAreaEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
	
class AddImageSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    ImageEntry = forms.ImageField(label='')
    def __init__(self, *args, **kwargs):
        super(AddImageSearch, self).__init__(*args, **kwargs)		
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})	
		
class AddAudioSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    AudioEntry = forms.FileField(label='')
    def __init__(self, *args, **kwargs):
        super(AddAudioSearch, self).__init__(*args, **kwargs)
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})	
		
class AddVideoSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    VideoEntry = forms.FileField(label='')
    def __init__(self, *args, **kwargs):
        super(AddVideoSearch, self).__init__(*args, **kwargs)
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
		
class AddBooleanSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    BooleanEntry = forms.BooleanField(initial=False, required=False,label='')
    def __init__(self, *args, **kwargs):
        super(AddBooleanSearch, self).__init__(*args, **kwargs)
        self.fields['BooleanEntry'].widget.attrs.update({'class': 'form-control d-flex justify-content-between'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
		
class AddEmailSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    EmailEntry = forms.EmailField(label='')
    Op = forms.ChoiceField(choices=tuple(enumerate(Operand)),label='')
    def __init__(self, *args, **kwargs):
        super(AddEmailSearch, self).__init__(*args, **kwargs)
        self.fields['EmailEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
        self.fields['Op'].widget.attrs.update({'class': 'form-control'})
		
class AddIpAddressSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    IpAddressEntry = forms.GenericIPAddressField(label='')
    def __init__(self, *args, **kwargs):
        super(AddIpAddressSearch, self).__init__(*args, **kwargs)
        self.fields['IpAddressEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
		
class AddUrlSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    UrlEntry = forms.URLField(label='')
    def __init__(self, *args, **kwargs):
        super(AddUrlSearch, self).__init__(*args, **kwargs)
        self.fields['UrlEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
		
class AddDateSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "after", "before"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    DateEntry = forms.DateField(label='')
    def __init__(self, *args, **kwargs):
        super(AddDateSearch, self).__init__(*args, **kwargs)
        self.fields['DateEntry'].widget.attrs.update({'class': 'form-control','type': 'date'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
		
class AddTimeSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "after", "before"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    TimeEntry = forms.TimeField(label='')
    def __init__(self, *args, **kwargs):
        super(AddTimeSearch, self).__init__(*args, **kwargs)
        self.fields['TimeEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})		
		
class AddDateTimeSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "after", "before"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    DateTimeEntry = forms.DateTimeField(label='')
    def __init__(self, *args, **kwargs):
        super(AddDateTimeSearch, self).__init__(*args, **kwargs)
        self.fields['DateTimeEntry'].widget.attrs.update({'class': 'form-control','type': 'datetime-local'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})	
		
class AddIntegerSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "less than","more than"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    IntegerEntry = forms.IntegerField(label='')
    def __init__(self, *args, **kwargs):
        super(AddIntegerSearch, self).__init__(*args, **kwargs)
        self.fields['IntegerEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})		
		
class AddDecimalSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "less than","more than"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    DecimalEntry = forms.DecimalField(label='')
    def __init__(self, *args, **kwargs):
        super(AddDecimalSearch, self).__init__(*args, **kwargs)
        self.fields['DecimalEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})		
		
class AddFloatSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "less than","more than"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    FloatEntry = forms.FloatField(label='')
    def __init__(self, *args, **kwargs):
        super(AddFloatSearch, self).__init__(*args, **kwargs)
        self.fields['FloatEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
		
class AddEnumaratedSearch(forms.Form):	
    def __init__(self, *args, **kwargs):
        Operand = ["","AND", "OR"]	
        enum = kwargs.pop('en')
        name = kwargs.pop('nm')
        super(AddEnumaratedSearch, self).__init__(*args, **kwargs)
        ChoiceList = ["equals", "contains","not equal","not contain"]
        self.fields['Condition'] = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
        self.fields['EnumaratedEntry'] = forms.ChoiceField(choices=tuple(enumerate(enum)),label='')
        self.fields['EnumaratedEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
        contextName={}
        contextName['name']=name
        cnName = contextName.get(name,name)
        super(AddEnumaratedSearch, self).add_prefix(cnName)
        
class AddLocationSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    LocationEntry = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(AddLocationSearch, self).__init__(*args, **kwargs)
        self.fields['LocationEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})		
		
class AddTagSearch(forms.Form):
    Operand = ["","AND", "OR"]
    ChoiceList = ["equals", "contains","not equal","not contain"]
    Condition = forms.ChoiceField(choices=tuple(enumerate(ChoiceList)),label='')
    TagEntry = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(AddTagSearch, self).__init__(*args, **kwargs)
        self.fields['TagEntry'].widget.attrs.update({'class': 'form-control'})
        self.fields['Condition'].widget.attrs.update({'class': 'form-control'})
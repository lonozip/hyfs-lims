from django import forms
from .models import Standard_radiation_hygiene

class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard_radiation_hygiene
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(StandardForm, self).__init__(*args, **kwargs)
        
        # 为标准名称生成下拉选项
        existing_names = Standard_radiation_hygiene.objects.values_list('name', flat=True).distinct()
        name_choices = [(name, name) for name in existing_names if name]
        if name_choices:
            # 添加"其他"选项
            name_choices.append(('other', '其他'))
            self.fields['name'] = forms.ChoiceField(
                choices=name_choices,
                required=True,
                label='标准名称'
            )
        
        # 为标准类型生成下拉选项
        existing_types = Standard_radiation_hygiene.objects.values_list('standard_type', flat=True).distinct()
        type_choices = [(typ, typ) for typ in existing_types if typ]
        if type_choices:
            # 添加"其他"选项
            type_choices.append(('other', '其他'))
            self.fields['standard_type'] = forms.ChoiceField(
                choices=type_choices,
                required=True,
                label='标准类型'
            )
        
        # 为标准编号生成下拉选项
        existing_ids = Standard_radiation_hygiene.objects.values_list('standard_id', flat=True).distinct()
        id_choices = [(sid, sid) for sid in existing_ids if sid]
        if id_choices:
            # 添加"其他"选项
            id_choices.append(('other', '其他'))
            self.fields['standard_id'] = forms.ChoiceField(
                choices=id_choices,
                required=True,
                label='标准编号'
            )
    
    def clean_standard_id(self):
        """重写标准编号的验证，允许重复"""
        standard_id = self.cleaned_data.get('standard_id')
        # 直接返回标准编号，不进行唯一性验证
        return standard_id
    
    def clean(self):
        cleaned_data = super(StandardForm, self).clean()
        
        # 处理标准名称的"其他"选项
        name = cleaned_data.get('name')
        if name == 'other' and 'name_other' in self.data:
            cleaned_data['name'] = self.data['name_other']
        
        # 处理标准类型的"其他"选项
        standard_type = cleaned_data.get('standard_type')
        if standard_type == 'other' and 'standard_type_other' in self.data:
            cleaned_data['standard_type'] = self.data['standard_type_other']
        
        # 处理标准编号的"其他"选项
        standard_id = cleaned_data.get('standard_id')
        if standard_id == 'other' and 'standard_id_other' in self.data:
            cleaned_data['standard_id'] = self.data['standard_id_other']
        
        return cleaned_data

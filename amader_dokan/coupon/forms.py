from django import forms


class CouponCodeForm(forms.form):
    code = forms.CharField()

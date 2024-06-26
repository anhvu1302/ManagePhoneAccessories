﻿from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm,
)

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import re,base64
import secrets
import smtplib
from base64 import urlsafe_b64encode
from django.utils.http import urlsafe_base64_encode


class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:

            user = authenticate(username=username, password=password)
            if user is None:

                raise forms.ValidationError("Inconrrect Password or Username")
            else:
                login(self.request, user)
        return cleaned_data


class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="username", max_length=30)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    def clean_password2(self):
        if "password1" in self.cleaned_data:
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Passwords do NOT match")

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:

            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Email already exists")

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not re.search(r"^\w+$", username):
            raise forms.ValidationError("Invalid character ")

        try:

            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already exists")

    def save(self):

        User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )


class RecoveryForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.uidb64 = kwargs.pop("uidb64", None)
        self.token = kwargs.pop("token", None)
        super(RecoveryForm, self).__init__(*args, **kwargs)

        if self.uidb64 is None or self.token is None:
            raise ValueError("uidb64 and token must be provided")

    def clean_password(self):

        return new_password

    def save(self, new_password):

        uid = urlsafe_base64_decode(self.uidb64).decode("utf-8")

        user = User.objects.get(id=uid)

        if not default_token_generator.check_token(user, self.token):
            raise forms.ValidationError("Invalid token")

        user.set_password(new_password)
        user.save()


class IdentifyForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required")

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Email does not exist")

        return email

    def send_password_reset_email(self, request):

        email = self.clean_email()

        token = secrets.token_urlsafe(32)

        user = User.objects.get(email=email)

        # Tạo token để sử dụng trong URL khôi phục mật khẩu
        token = default_token_generator.make_token(user)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse("recovery", kwargs={"uidb64": uidb64, "token": token})

        # Xây dựng đường link hoàn chỉnh
        full_reset_url = request.build_absolute_uri(reset_url)

        # Gửi email khôi phục mật khẩu
        sender_email = "tiki.statistic@gmail.com"
        password = "vpG)b#T6^CN9/x3"
        receiver_email = email  # Gửi email đến địa chỉ email của người dùng
        subject = "Password Reset Request"

        # Tạo một email có dạng HTML
        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Nội dung của email
        html = f"""\
        <html>
          <body>
            <p>Hi,</p>
            <p>We received a request to reset your password. Click the link below to reset it:</p>
            <p><a href="{full_reset_url}">{full_reset_url}</a></p>
            <p>If you didn't request this, you can ignore this email.</p>
          </body>
        </html>
        """

        # Thêm nội dung HTML vào email
        message.attach(MIMEText(html, "html"))

        # Kết nối đến máy chủ SMTP và gửi email
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

class OrderForm(forms.Form):
    user_id = forms.IntegerField(
        label="User ID" ,
        widget=forms.HiddenInput(),
        error_messages= {
            "required": "Vui lòng đăng nhập để đặt hàng",

        }
    )  # Assuming you have the user ID as an integer
    total_amount = forms.IntegerField(
        required=True,
        label="Total Amount", 
        error_messages= {
            "required": "CÓ VẤN ĐỀ @@",

        },
        widget=forms.HiddenInput(attrs = {}), #Được lấy từ cart đưa vào
    )
    phone_number = forms.CharField(
        required=True,
        max_length=12, 
        min_length=12 ,
        error_messages= {
            "required": "Vui lòng nhập số điện thoại",
            "max_length": "Số điện thoại không hợp lệ",
            "min_length": "Số điện thoại không hợp lệ"

        },
        label="Phone Number",
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    address = forms.CharField(
        required=True,
        min_length=20,
        error_messages= {
            "required":"Địa chỉ không được trống!"
        },
        label="Address", 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    

    def save(self):
        user_id = self.cleaned_data["user_id"]
        total_amount = self.cleaned_data["total_amount"]
        phone_number = self.cleaned_dataT["phone_number"]
        address = self.cleaned_data["address"]

        #Save to Orders
        user = User.objects.get(id = user_id)
        newOrder = Orders(
            UserID = user, 
            TotalAmount = int(total_amount),
            PhoneNumber = phone_number,
            Address = address
        )
        newOrder.save()

        #Get items in Cart and add each them to OrderDetails
        cart_items = Cart.objects.filter(UserID=user)
        for item in cart_items:
            newOrderDetails = OrderDetails(
                OrderID = newOrder,
                AccessoryID = item.AccessoryID,
                Quantity = item.Quantity,
                UnitPrice = item.AccessoryID.Price
            )
            newOrderDetails.save()
        #After payment, delete item in cart of user
        Cart.objects.filter(UserID=user).delete()            

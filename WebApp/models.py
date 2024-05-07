from django.db import models

class ParentCategories(models.Model):
    ParentCategoryName = models.CharField(max_length=100)

class Categories(models.Model):
    CategoryName = models.CharField(max_length=100)
    ParentCategoryID = models.ForeignKey(
        ParentCategories, on_delete=models.CASCADE, related_name="categories"
    )

class Accessories(models.Model):
    Name = models.CharField(max_length=100)
    Price = models.BigIntegerField
    Discount = models.IntegerField
    Image = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    StockQuantity = models.IntegerField
    CategoryID = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name="accessories"
    )

class Users(models.Model):
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Email = models.CharField(max_length=100)
    Avatar = models.CharField(max_length=255)
    RoleName = models.CharField(max_length=50)

class Cart(models.Model):
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="carts")
    AccessoryID = models.ForeignKey(
        Accessories, on_delete=models.CASCADE, related_name="carts"
    )
    Quantity = models.IntegerField

class Orders(models.Model):
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="orders")
    TotalAmount = models.BigIntegerField
    PhoneNumber = models.CharField(max_length=11)
    Address = models.CharField(max_length=255)
    OrderDate = models.DateTimeField(auto_now_add=True)

class OrderDetails(models.Model):
    OrderID = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_details")
    AccessoryID = models.ForeignKey(
        Accessories, on_delete=models.CASCADE, related_name="order_details"
    )
    Quantity = models.IntegerField
    UnitPrice = models.BigIntegerField

class ImportAccessory(models.Model):
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="imports")
    TotalAmount = models.BigIntegerField
    ImportDate = models.DateTimeField(auto_now_add=True)

class ImportDetail(models.Model):
    ImportAccessoryID = models.ForeignKey(
        ImportAccessory, on_delete=models.CASCADE, related_name="import_details"
    )
    AccessoryID = models.ForeignKey(
        Accessories, on_delete=models.CASCADE, related_name="import_details"
    )
    Quantity = models.IntegerField
    UnitPrice = models.BigIntegerField
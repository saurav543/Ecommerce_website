from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category table implementd with MPTTModel
    """
    name = models.CharField(
        verbose_name=_('Category name'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_(
        "category safe url"), max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Product tabel will provide a list of the different types of the product  that are for sale.
    """

    name = models.CharField(verbose_name=_("Product Name"), help_text=_(
        'Required'), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProudctSpecification(models.Model):
    """
    The product specification table contains product specification or features for the product types.
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_(
        "Name"), help_text=_("Required"), max_length=255,)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The product table containing all product item
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_(
        'title'), help_text=_("Required"), max_length=255)
    description = models.TextField(verbose_name=_(
        "Description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be lie in 0 to 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        help_text=_("maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be lie in 0 to 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False),
    updated_at = models.DateTimeField(_("updatd at"), auto_now=True)
    user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="user_wishlist",blank=True)
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductSpecificationValue(models.Model):
    """
    The ProductSpecificationValue  table holds each of the products indivisual specification or bespoke feature
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(
        ProudctSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 word)"),
        max_length=255

    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")


class ProductImage(models.Model):
    """
     Product image table
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(verbose_name=_("Image"), help_text=_(
        "Upload a product image"), upload_to="product_image/", default="product_image/default.png",)
    alt_text = models.CharField(verbose_name=_("Alternative Text"), help_text=_(
        "Please add alternative text"),
        max_length=255,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False),
    updated_at = models.DateTimeField(_("updatd at"), auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return self.alt_text

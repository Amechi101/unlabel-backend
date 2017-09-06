from django import template
from oscar.core.loading import get_class

register = template.Library()

Line = get_class('basket.models','Line')
LineAttribute = get_class('basket.models','LineAttribute')
Product = get_class('catalogue.models','Product')
ProductAttribute = get_class('catalogue.models','ProductAttribute')
ProductAttributeValue = get_class('catalogue.models','ProductAttributeValue')

@register.assignment_tag
def get_line_size(line_id):
    line = Line.objects.get(pk=line_id)
    product = Product.objects.get(id=line.product.pk)
    try:
        attr_value = ProductAttributeValue.objects.get(product=product,attribute__code__iexact='size')
        size = attr_value.value_option
    except:
        size = ''

    return "size : " + str(size)


@register.assignment_tag
def get_inch_value(num):
    try:
        inch_value = int(int(num)*0.393)
    except:
        inch_value = "Not found"
    return inch_value


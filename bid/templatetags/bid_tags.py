import re
from bid.models import BidMaterial
from django import template
from django.utils.safestring import mark_safe
from materials.models import Material


register = template.Library()


@register.filter
def get_material_description(material_id):
    material = Material.objects.get(material_id=material_id)
    return mark_safe(material.description)


@register.filter
def get_manufacturer(material_id):
    material = Material.objects.get(material_id=material_id)
    return mark_safe(material.manufacturer)


@register.filter
def get_manufacturer_number(material_id):
    material = Material.objects.get(material_id=material_id)
    return mark_safe(material.manufacturer_number)


@register.filter
def format_unit_of_measure(unit_of_measure):
    if unit_of_measure == "1":
        return 'EA'
    elif unit_of_measure == "100":
        return '100EA'
    elif unit_of_measure == "1000":
        return '1000EA'
    else:
        return ''


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def get_image_url(material, material_vendors):
    for material_vendor in material_vendors:
        if material_vendor.vendor.vendor_name == 'graybar':
            if material_vendor.material.manufacturer_number.upper() == material.manufacturer_number.upper():
                image_url = material_vendor.vendor_image_link
                if image_url and image_url.lower() not in {'none', 'n/a', 'na', 'null'}:
                    return image_url
    return None


@register.filter
def get_vendor_price(material, material_vendors):
    vendor_prices = {}
    for material_vendor in material_vendors:
        if material_vendor.material.material_id == material.material_id:
            vendor_data = {
                'price': material_vendor.vendor_unit_price,
                'unit_of_measure': material_vendor.vendor_unit_of_measure,
                'product_link': material_vendor.vendor_product_link,
            }
            if material_vendor.vendor.vendor_name == 'anixter/wesco':
                vendor_prices['anixter'] = vendor_data
            elif material_vendor.vendor.vendor_name == 'graybar':
                vendor_prices['graybar'] = vendor_data
            elif material_vendor.vendor.vendor_name == 'rexel (platt electric)':
                vendor_prices['rexel'] = vendor_data
            else:
                vendor_prices[material_vendor.vendor.vendor_name] = vendor_data
    return vendor_prices


@register.filter
def get_per_price(vendor_price, unit_of_measure):
    if unit_of_measure in {'1', 'ea', 'each'}:
        return vendor_price
    elif unit_of_measure in {'100', '100ea', '100ft'}:
        return vendor_price / 100
    elif unit_of_measure in {'1000', '1000ea', '1000ft'}:
        return vendor_price / 1000
    else:
        return None


@register.filter
def get_uom_name(unit_of_measure):
    uom_name = re.sub(r'\d+', '', unit_of_measure)
    return uom_name.strip()

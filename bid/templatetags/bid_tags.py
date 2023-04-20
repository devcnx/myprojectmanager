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
def get_total_price(bid_material):
    quantity = bid_material['quantity']
    unit_of_measure = bid_material['unit_of_measure']
    unit_price = bid_material['unit_price']
    if unit_of_measure == "1":
        return "$ {:.2f}".format(quantity * unit_price)
    elif unit_of_measure == "100":
        return "$ {:.2f} (100{})".format((quantity * unit_price) / 100, bid_material['unit_display'])
    elif unit_of_measure == "1000":
        return "$ {:.2f} (1000{})".format((quantity * unit_price) / 1000, bid_material['unit_display'])
    else:
        return "N/A"


@register.filter
def get_image_url(material, material_vendors):
    for material_vendor in material_vendors:
        if material_vendor.material.material_id == material.material_id:
            if material_vendor.vendor_image_link and material_vendor.vendor_image_link != 'NULL':
                return material_vendor.vendor_image_link
    return None


@register.filter
def get_vendor_price(material, material_vendors):
    vendor_prices = {}
    for material_vendor in material_vendors:
        if material_vendor.material.material_id == material.material_id:
            vendor_data = {
                'price': material_vendor.vendor_unit_price,
                'unit_of_measure': material_vendor.vendor_unit_of_measure
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

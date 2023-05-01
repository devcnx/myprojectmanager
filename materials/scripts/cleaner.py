from dataclasses import dataclass
from materials.models import MaterialVendor


def clean_material_vendors():
    material_vendors = MaterialVendor.objects.all()
    for material_vendor in material_vendors:
        material_vendor.vendor_part_number = material_vendor.vendor_part_number.lower(
        ).strip() if material_vendor.vendor_part_number else None
        material_vendor.vendor_unit_of_measure = material_vendor.vendor_unit_of_measure.lower(
        ).strip() if material_vendor.vendor_unit_of_measure else None
        material_vendor.vendor_unit_of_measure = material_vendor.vendor_unit_of_measure.replace(
            'each', 'ea') if material_vendor.vendor_unit_of_measure else None
        material_vendor.vendor_unit_of_measure = material_vendor.vendor_unit_of_measure.replace(
            'box', 'ea') if material_vendor.vendor_unit_of_measure else None
        material_vendor.vendor_unit_of_measure = material_vendor.vendor_unit_of_measure.replace(
            'pack', 'ea') if material_vendor.vendor_unit_of_measure else None
        material_vendor.vendor_unit_of_measure = material_vendor.vendor_unit_of_measure.replace(
            'n/a', 'ea') if material_vendor.vendor_unit_of_measure else None
        material_vendor.vendor_product_link = material_vendor.vendor_product_link.lower(
        ).strip() if material_vendor.vendor_product_link else None
        material_vendor.vendor_image_link = material_vendor.vendor_image_link.lower(
        ).strip() if material_vendor.vendor_image_link else None
        material_vendor.save()

    print('Material Vendors Cleaned')

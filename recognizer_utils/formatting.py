from datetime import date, time
from time import strftime, strptime

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join("Page #{}: {}".format(region.page_number, format_polygon(region.polygon)) for region in bounding_regions)

def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

def print_receipts(result, print_items = False):
    indent = '   '
    docs = []
    for receipt in result.documents:
        doc = {}
        name = 'DocType'
        print(f'{indent}{name.ljust(30)}', receipt.doc_type )
        doc[name] = receipt.doc_type
        for name, field in receipt.fields.items():
            if name == "Items":
                if print_items:
                    print("Receipt Items:")
                    for idx, item in enumerate(field.value):
                        print("...Item #{}".format(idx+1))
                        for item_field_name, item_field in item.value.items():
                            print("......{}: {} has confidence {}".format(
                                item_field_name, item_field.value, item_field.confidence))
            else:
                if field.value is not None and isinstance(field.value, (int, float, date, time, str)):
                    print(f'{indent}{name.ljust(30)} {field.value}')
                    doc[name] = field.value
        docs.append(doc)
    return docs


def cast_datetime_to_str(data):
    result = dict()
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = cast_datetime_to_str(value)
        elif isinstance(value, date):
            result[key] = value.strftime('%F')
        elif isinstance(value, time):
            result[key] = value.strftime('%H:%M:%S')
        else:
            result[key] = value
    return result
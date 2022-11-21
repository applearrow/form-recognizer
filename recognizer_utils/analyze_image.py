from genericpath import exists
import json
import pickle
import time
from decouple import config
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from recognizer_utils.formatting import cast_datetime_to_str, format_bounding_region, format_polygon, print_receipts
from termcolor import colored

endpoint = config('FORM_RECOGNIZER_ENDPOINT')
key = config('FORM_RECOGNIZER_KEY')

def analyze_image( image: str, results_folder: str):
    
    print (colored(f'Analyzing {image}...', 'white'))
    pickle_folder = 'pickle'

    path_to_file = f'{pickle_folder}/{image}.pkl'
    file_exists = exists(path_to_file)
    if (not file_exists):
        # Analyze the image using form recognizer
        docUrl = f'https://raw.githubusercontent.com/applearrow/applearrow.github.io/main/receipts/{image}'
        document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        start = time.time()
        poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-receipt", docUrl)
        result = poller.result()
        end = time.time()
        print(colored(f'Analysis for {image} took {end - start} seconds'), 'white')
        # Save the result for future reference
        with open(f'{pickle_folder}/{image}.pkl', 'wb+') as f:
            pickle.dump(result, f)
    else:
        # Just load the previous analysis result from a pickle file
        with open(f'{pickle_folder}/{image}.pkl', 'rb') as f:
            result = pickle.load(f)
        print(colored(f'Reading pickle...', 'white'))

    docs = print_receipts(result)
    first_doc = docs[0]
    if (first_doc):
        # Save the output to a file 
        with open(f'{results_folder}/{image}.json', 'w+', encoding='utf-8') as f:
            json.dump(cast_datetime_to_str(first_doc), f, indent=2)

    return 
    

    for style in result.styles:
        if style.is_handwritten:
            print("Document contains handwritten content: ")
            print(",".join([result.content[span.offset:span.offset + span.length] for span in style.spans]))

    print("----Key-value pairs found in document----")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key:
            print(
                    "Key '{}' found within '{}' bounding regions".format(
                        kv_pair.key.content,
                        format_bounding_region(kv_pair.key.bounding_regions),
                    )
                )
        if kv_pair.value:
            print(
                    "Value '{}' found within '{}' bounding regions\n".format(
                        kv_pair.value.content,
                        format_bounding_region(kv_pair.value.bounding_regions),
                    )
                )

    for page in result.pages:
        print("----Analyzing document from page #{}----".format(page.page_number))
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

        for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_polygon(line.polygon),
                )
            )

        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

        for selection_mark in page.selection_marks:
            print(
                "...Selection mark is '{}' within bounding box '{}' and has a confidence of {}".format(
                    selection_mark.state,
                    format_polygon(selection_mark.polygon),
                    selection_mark.confidence,
                )
            )

    for table_idx, table in enumerate(result.tables):
        print(
            "Table # {} has {} rows and {} columns".format(
                table_idx, table.row_count, table.column_count
            )
        )
        for region in table.bounding_regions:
            print(
                "Table # {} location on page: {} is {}".format(
                    table_idx,
                    region.page_number,
                    format_polygon(region.polygon),
                )
            )
        for cell in table.cells:
            print(
                "...Cell[{}][{}] has content '{}'".format(
                    cell.row_index,
                    cell.column_index,
                    cell.content,
                )
            )
            for region in cell.bounding_regions:
                print(
                    "...content on page {} is within bounding box '{}'\n".format(
                        region.page_number,
                        format_polygon(region.polygon),
                    )
                )
    print("----------------------------------------")

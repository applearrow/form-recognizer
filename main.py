from os.path import exists
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from recognizer_utils.compare_results import compare_results
from recognizer_utils.analyze_image import analyze_image

def analyze_images( images: list[str], results_folder: str):
    for image in images:
        path_to_file = f'{results_folder}/{image}.json'
        file_exists = exists(path_to_file)
        if (not file_exists):
            analyze_image(image, results_folder)

if __name__ == "__main__":
    results_folder = 'results'
    images = [ 'gas1.png' ]
    # images = [
    #     "British1.jpg", "British6.jpg",    "french1.jpg",    "gas1.png",        "mercadona.jpg",   "parking3.png",    "portales.jpg",    "receipt0.png",  "wallmart.png",
    #     "British2.jpg", "Tagliatella.pdf", "french2.png",    "gas2.png",        "oister.jpg",      "pizza.jpg",       "pub.jpg",         "receipt8.jpg",  "white_castle.jpg",
    #     "British3.jpg", "bestiari.jpg",    "french3.jpg",    "gas3.jpg",        "optica.jpg",      "plane1.jpg",      "quesos.jpg",      "sheraton.jpg",
    #     "British4.jpg", "bodega.jpg",      "french4.jpg",    "leroy1.jpg",      "parking1.png",    "porcos.jpg",      "quick.jpg",       "sncf.jpg",
    #     "British5.jpg", "creperie.jpg",    "french5.jpg",    "mark_ticket.jpg", "parking2.png",    "porquets.jpg",    "raco.jpg",        "train1.jpg"
    # ]
    analyze_images(images, results_folder)
    compare_results('correct_values.json')


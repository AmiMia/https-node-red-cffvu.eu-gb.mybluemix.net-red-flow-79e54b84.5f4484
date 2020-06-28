import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='Vi7lrOVTqCDLnxs2n0McsYbGVS9G8Gb3-xWsMF-NUMeM')

with open('./Test2.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
	classifier_ids='Fire_504844078').get_result()
print(json.dumps(classes, indent=2))

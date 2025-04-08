from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model_id = 'iic/cv_tinynas_human-detection_damoyolo'
input_location = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/image_detection.jpg'

human_detection = pipeline(Tasks.domain_specific_object_detection, model=model_id)
result = human_detection(input_location)
print("result is : ", result)
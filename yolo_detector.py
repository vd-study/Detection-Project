import matplotlib.pyplot as plt
from inheritance_function import *
from gluoncv import model_zoo, data, utils


def get_picture_from_server(folder,img_name):
    img_path = folder+'/'+img_name

    net = model_zoo.get_model('yolo3_darknet53_voc', pretrained=True)

    im_fname = img_path
    # short = 512
    x, img = data.transforms.presets.yolo.load_test(im_fname, short=512)

    class_IDs, scores, bounding_boxs = net(x)

    ax = plot_bbox_custom(img, bounding_boxs[0], scores[0],class_IDs[0],thresh=0.65 ,class_names=net.classes)
    plt.axis('off')
    filename = 'ready/{}'.format(img_name)
    plt.savefig('static/' + filename)
    return filename


import struct
import sys
from models import *
from tool.utils import *
from tool.darknet2pytorch import *
from tool import torch_utils
model = Darknet(sys.argv[1], (608, 608))
weights = sys.argv[2]
device = torch_utils.select_device('0')
if weights.endswith('.pth'):  # pytorch format
    model.load_state_dict(torch.load(weights, map_location=device)['model'])
else:  # darknet format
    load_weights(model, weights)

f = open('yolov4.wts', 'w')
f.write('{}\n'.format(len(model.state_dict().keys())))
for k, v in model.state_dict().items():
    vr = v.reshape(-1).cpu().numpy()
    f.write('{} {} '.format(k, len(vr)))
    for vv in vr:
        f.write(' ')
        f.write(struct.pack('>f',float(vv)).hex())
    f.write('\n')


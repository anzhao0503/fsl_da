# import os.path as osp
# from PIL import Image

# from torch.utils.data import Dataset
# from torchvision import transforms


# ROOT_PATH = './materials/'


# class MiniImageNet(Dataset):

#     def __init__(self, setname):
#         csv_path = osp.join(ROOT_PATH, setname + '.csv')
#         lines = [x.strip() for x in open(csv_path, 'r').readlines()][1:]

#         data = []
#         label = []
#         lb = -1

#         self.wnids = []

#         for l in lines:
#             name, wnid = l.split(',')
#             path = osp.join(ROOT_PATH, 'images', name)
#             if wnid not in self.wnids:
#                 self.wnids.append(wnid)
#                 lb += 1
#             data.append(path)
#             label.append(lb)

#         self.data = data
#         self.label = label

#         self.transform = transforms.Compose([
#             transforms.Resize(84),
#             transforms.CenterCrop(84),
#             transforms.ToTensor(),
#             transforms.Normalize(mean=[0.485, 0.456, 0.406],
#                                  std=[0.229, 0.224, 0.225])
#         ])

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, i):
#         path, label = self.data[i], self.label[i]
#         image = self.transform(Image.open(path).convert('RGB'))
#         return image, label
import os
from PIL import Image

from torch.utils.data import Dataset
from torchvision import transforms
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class MiniImageNet(Dataset):

    def __init__(self, root='../dataset/mini-imagenet/train'):
        self.root = root
        self.data = []
        self.label = []
        self.label_dict = self._get_label()
        self._load_dataset()

        self.transform = transforms.Compose([
            transforms.Resize(84),
            transforms.CenterCrop(84),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def _get_label(self):
        labels = {}
        idx = 0
        train_list = os.listdir(self.root)
        for name in train_list:
            labels[name] = idx
            idx += 1
        return labels

    def _load_dataset(self):
        path = self.root
        subdirs = os.listdir(path)
        for subdir in subdirs:
            labels = self.label_dict[subdir]
            imgs = os.listdir(os.path.join(path, subdir))
            for img in imgs:
                img_path = os.path.join(path, subdir, img)
                self.data.append(img_path)
                self.label.append(labels)

    def __getitem__(self, i):
        path, label = self.data[i], self.label[i]
        image = self.transform(Image.open(path).convert('RGB'))
        return image, label

    def __len__(self):
        return len(self.data)
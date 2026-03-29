import torch
import torch.nn as nn
from torchvision import models

class VisionPriceNet(nn.Module):
    def __init__(self):
        super().__init__()

        # ✅ SAME AS TRAINING (ResNet50)
        resnet = models.resnet50(weights=None)
        self.cnn = nn.Sequential(*list(resnet.children())[:-1])

        self.image_head = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 128)
        )

        self.tabular_net = nn.Sequential(
            nn.Linear(4, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU()
        )

        self.fusion = nn.Sequential(
            nn.Linear(128 + 32, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, img, feat):
        batch_size = img.size(0)

        imgs_split = img.view(batch_size, 4, 3, 224, 224)

        cnn_feats = []

        for i in range(4):
            x = imgs_split[:, i]
            x = self.cnn(x)
            x = x.view(batch_size, -1)
            cnn_feats.append(x)

        img_feat = torch.stack(cnn_feats).mean(dim=0)
        img_feat = self.image_head(img_feat)

        tab_feat = self.tabular_net(feat)

        x = torch.cat([img_feat, tab_feat], dim=1)
        out = self.fusion(x)

        return out
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
from KD_Lib.RKD import RKDLoss
from KD_Lib.common import BaseClass
from KD_Lib.attention import ATLoss
from copy import deepcopy

class attention(BaseClass):
    def __init__(self, teacher_model, student_model, train_loader, val_loader, optimizer_teacher, optimizer_student, loss='MSE', temp=20.0, distil_weight=0.5, device='cpu'):
        super(attention, self).__init__(
            teacher_model, 
            student_model,
            train_loader,
            val_loader, 
            optimizer_teacher,
            optimizer_student,
            loss,
            temp,
            distil_weight,
            device
        ) 

        self.loss_fn = ATLoss()

    def calculate_kd_loss(self, y_pred_student, y_pred_teacher, y_true):
        soft_student_out = F.softmax(y_pred_student[0]/self.temp, dim=1)
        loss = (1 - self.distil_weight) * F.cross_entropy(soft_student_out, y_true)
        loss += self.distil_weight * self.loss_fn(y_pred_teacher, y_pred_student)

        return loss
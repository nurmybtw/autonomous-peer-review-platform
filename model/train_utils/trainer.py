import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

class Trainer:
    def __init__(self, 
                 model,
                 train_dataset, 
                 test_dataset, 
                 compute_metrics, 
                 lr=1e-3,
                 data_collator=None, 
                 task_config='multi-label-classification'):
        self.model = model
        self.data_collator = data_collator
        self.train_dataset = train_dataset
        self.test_dataset = test_dataset
        self.compute_metrics = compute_metrics
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.task_config = task_config
        if task_config == 'multi-label-classification':
            self.criterion = nn.BCEWithLogitsLoss()
        elif task_config == 'multi-class-classification':
            self.criterion = nn.CrossEntropyLoss()
        
    def train(self, 
              num_epochs, 
              batch_size=8, 
              save_checkpoint_rate=2, 
              checkpoint_path='',
              resume_from_checkpoint=None):
        trainloader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True)
        init_epoch = 0
        if resume_from_checkpoint:
            checkpoint = torch.load(resume_from_checkpoint, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            init_epoch = checkpoint['epoch']
        for epoch in range(init_epoch, init_epoch + num_epochs):
            self.model.train()
            train_loss = 0.0
            for inputs, targets in tqdm(trainloader):
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                self.optimizer.zero_grad()
                outputs, _ = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()
                train_loss += loss.item()
            avg_train_loss = train_loss / len(trainloader)
            print(f'Epoch {epoch + 1}, Loss: {avg_train_loss}')
            self.test(batch_size=batch_size)
            if (epoch + 1) % save_checkpoint_rate == 0:
                torch.save({
                    'epoch': epoch + 1,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                }, f'{checkpoint_path}/checkpoint_epoch_{epoch+1}.pth')
                
    def test(self, batch_size=8):
        testloader = DataLoader(self.test_dataset, batch_size=batch_size, shuffle=False)
        metrics = []
        with torch.no_grad():
            self.model.eval()
            for inputs, targets in tqdm(testloader):
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                outputs, _ = self.model(inputs)
                metrics.append(self.compute_metrics((outputs.cpu().numpy(), targets.cpu().numpy()), 
                                                    task_config=self.task_config))
        # Average of metrics across batches
        avg_metrics = {}
        count = len(metrics)
        for entry in metrics:
            for metric, value in entry.items():
                if metric not in avg_metrics:
                    avg_metrics[metric] = 0
                avg_metrics[metric] += value
        for metric in avg_metrics: avg_metrics[metric] /= count
        print(avg_metrics)
        
    def save_model(self, output_path):
        pass
from backend.model.rnn import RNN
import torch
import string
import numpy as np
import unicodedata

class Utils:
    def __init__(self) -> None:
        np.set_printoptions(suppress=True)
        self.all_letters = string.ascii_letters + " .,;'"
        self.n_letters = len(self.all_letters)
        self.n_categories = 18
        self.n_hidden = 128

        self.n_predictions = 5

        self.device = torch.device('cpu')
        self.all_categories =['Arabic',
                                'Chinese',
                                'Czech',
                                'Dutch',
                                'English',
                                'French',
                                'German',
                                'Greek',
                                'Irish',
                                'Italian',
                                'Japanese',
                                'Korean',
                                'Polish',
                                'Portuguese',
                                'Russian',
                                'Scottish',
                                'Spanish',
                                'Vietnamese']
        
        self.model = RNN(self.n_letters, self.n_hidden, self.n_categories)
        self.model.load_state_dict(torch.load('./backend/model/rnn.pth'))
        self.model.eval()

    def letterToIndex(self, letter):
        return self.all_letters.find(letter)
    
    def lineToTensor(self, line):
        tensor = torch.zeros(len(line), 1,self.n_letters)
        for li, letter in enumerate(line):
          tensor[li][0][self.letterToIndex(letter)] = 1
        return tensor  
    
    def unicodeToAscii(self,s):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
            and c in self.all_letters
             )

    def predict(self,name):
        name = self.unicodeToAscii(name)
        print(name)
        name = self.lineToTensor(name).to(self.device)
        self.model.hidden = self.model.init_hidden()
        output = self.model(name)
        topv, topi = output.topk(5, 1, True)
        probs = np.exp(topv.to(self.device).detach().numpy()) / (np.exp(topv.to(self.device).detach().numpy())).sum()
        probs*100
        predictions = []
        for i in range(self.n_predictions):
            value = probs[0][i].item()*100
            category_index = topi[0][i].item()
            predictions.append([round(value,1), self.all_categories[category_index]])
        return predictions



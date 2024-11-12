#
#Purpose: Определить порядок суммирования для ряда Sum_1^{\infty} (-1)^(n+1)/n, 
#         при котором сумма равна A
#

#%%
import numpy as np

from manim import *


#%% Геометрическая прогрессия
class SeriesGeometric:
    def __init__(self, b1, q):
        self.b1 = b1
        self.q = q
    
    def get_n_term(self, n):
        assert n>0, "Нумерация начинается с единицы"
        return self.b1 * self.q**(n-1)


    def get_every(self, every, n_of_every_kind):
        n_total = every * n_of_every_kind
        terms = [self.get_n_term(n) for n in range(1,1+n_total)]
        return [np.array(terms[i::every]) for i in range(every)]
    
    
    
    def get_every_cumsum(self, n, shape=(1,1)):
        """ shape -- сколько положительных, сколько отрицательных
            n     -- сколько членов каждого вида вернуть
        """
        n_pos, n_neg = n * shape[0], n * shape[1]
        pos,_ = self.get_every(2, n_pos)
        pos = np.sum(pos.reshape(-1, shape[0]), axis=1)
        
        _,neg = self.get_every(2, n_neg)
        neg = np.sum(neg.reshape(-1, shape[1]), axis=1)
        assert len(pos) == len(neg), 'Длины pos и neg должны совпадать'
        
        return np.cumsum(pos), np.cumsum(neg)

    
    

#%% Знакочередующийся гармонический ряд
class Series:
    def __init__(self, A):
        self.A = A
        self.A_cur = 0
        self.n_pos = 0
        self.n_neg = 0
        
        self.n_jumps = 0
        self.nn_pos = []
        self.nn_neg = []
        self.AA_cur = []
        self.ii = []
    
    
    def add_pos_to_limit(self):
        while self.A_cur <= self.A:
            self.n_pos += 1
            self.A_cur += 1 / (2 * self.n_pos - 1)
        self.nn_pos.append(self.n_pos)
        self.AA_cur.append(self.A_cur)

    
    def add_neg_to_limit(self):
        while self.A_cur >= self.A:
            self.n_neg += 1
            self.A_cur -= 1 / (2 * self.n_neg)
        self.nn_neg.append(self.n_neg)
        self.AA_cur.append(self.A_cur)
    

    def iterate(self, n_jumps):
        for i in range(n_jumps):
            self.add_pos_to_limit()
            self.add_neg_to_limit()
            self.n_jumps += 1
    
    
    def get_term(self, n):
        assert n>0, '1-based indexing'
        return (-1)**(n-1) / n
    
    def calc_sums_pos_neg(self, to_n):
        assert to_n%2 == 0, 'Предполагается, что количество элементов кратно двум'
        terms = [self.get_term(n) for n in range(1,1+to_n)]
        terms_pos = [term for term in terms if term > 0]
        terms_neg = [-term for term in terms if term < 0]
        return np.cumsum(terms_pos), np.cumsum(terms_neg)
    
    def calc_sums_pos_neg_neg(self, n_pos_elem_to_return):
        n = n_pos_elem_to_return
        pos = []
        neg = []
        n_pos = 0
        n_neg = 0
        i = 1
        while n_pos < n or n_neg < 2*n:
            term = self.get_term(i)
            if term > 0 and len(pos) < n:
                pos.append(term)
                n_pos += 1
            elif term < 0 and len(neg) < 2*n:
                neg.append(-term)
                n_neg += 1
            i += 1
        neg = np.array(neg).reshape(n,2)
        neg = np.sum(neg, axis=1)
        return np.cumsum(pos), np.cumsum(neg)

    
    def get_number_of_elements(self):
        nn_pos = np.array(self.nn_pos)
        nn_neg = np.array(self.nn_neg)
        d_pos = nn_pos[1:] - nn_pos[:-1]
        d_neg = nn_neg[1:] - nn_neg[:-1]
        return [nn_pos[0], *d_pos], [nn_neg[0], *d_neg]
    
    
    def get_pos_neg_amount_array(self):
        """ Создаёт массив количества членов ряда, которые были взяты попеременно
            из положительного и из отрицательного подрядов для достижения желаемого
            предела
        """
        res = []
        for np, nm in zip(*self.get_number_of_elements()):
            res.extend([np, nm])
        return res
        
        

#%% Тестирование
if __name__ == '__main__':
    if 1:
        ser = SeriesGeometric(0.5, -0.5)
        s1, s2 = ser.get_every_cumsum(10, shape=(1,1))
        print(s2-s1)

    if 0:
        import matplotlib.pyplot as plt
        ser = Series(1.5)
        ser.iterate(50)
        ii = list(range(len(ser.AA_cur)))
        
        plt.plot(ii, ser.AA_cur)
        plt.plot(ii[::2], ser.AA_cur[::2], ls='--')
        plt.plot(ii[1::2], ser.AA_cur[1::2], ls='--')
        plt.gca().axhline(ser.A, ls='--')
        
        plt.show()
        print(ser.get_number_of_elements())
        

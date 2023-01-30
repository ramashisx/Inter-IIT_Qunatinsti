from itertools import count
import math

class circular_array_volatility:
    def __init__(self,days):
        self.size = 0;
        self.pos = 0;
        self.max_size = days;
        self.compare_diff = [];
        for i in range(days):
            self.compare_diff.append(0);
        self.days = days;
        self.sqaure_term = 0;
        self.sum_term = 0;
        self.sd = 0
        self.max_mean = 0

    def add_element(self,elem):
        self.update_sd(elem);
        self.compare_diff[self.pos] = elem;
        self.pos = (self.pos+1)%self.max_size;

    def update_sd(self, elem):
        self.sqaure_term += elem*elem-self.compare_diff[self.pos]*self.compare_diff[self.pos];
        self.sum_term += elem-self.compare_diff[self.pos];
        self.size = max(self.size,self.pos+1);
        self.mean = self.sum_term/(self.size);
        self.max_mean = max(self.max_mean,self.mean)
        self.sd = math.sqrt(self.sqaure_term/self.size-self.mean*self.mean);
    
    def get_sd(self):
        return self.sd
    
    def get_mean(self):
        return self.mean

class circular_array_ema_sd:
    def __init__(self,days_ema,cal_sd):
        self.circular_array_volatility = circular_array_volatility(days_ema)
        self.days_ema = days_ema;
        self.ema = 0;
        self.cal_sd = cal_sd;

    def add_element(self,elem):
        if(self.cal_sd):
            self.circular_array_volatility.add_element(elem)
        self.update_ema(elem);

    def update_ema(self,diff):
        if(self.circular_array_volatility.size==1):
            self.ema = diff;
        else:
            alpha = 2.0/(1+self.days_ema);
            self.ema =  self.ema*(1-alpha)+alpha*diff;
    
    def get_sd(self):
        return self.circular_array_volatility.get_sd()

    def get_ema(self):
        return self.ema;

    
class circular_array_min_max:
    def __init__(self,days):
        self.size_min = 0;
        self.end_min = 0;
        self.start_min = 0;
        self.size_max = 0;
        self.end_max = 0;
        self.start_max = 0;
        self.max_size = days+1;
        self.compare_diff_min = [];
        self.compare_diff_max = [];
        for i in range(days+1):
            self.compare_diff_min.append([0,0]);
            self.compare_diff_max.append([0,0]);
        self.count = 0
        self.min_val = 0
        self.max_val = 0
        self.days = days;

    def add_element(self,elem):
        self.count = self.count+1
        while(self.size_min>0 and self.compare_diff_min[(self.end_min-1)%self.max_size][0]>=elem):
            self.end_min = (self.end_min-1)%self.max_size
            self.size_min=self.size_min-1
        self.compare_diff_min[self.end_min]=[elem,self.count]
        self.end_min = (self.end_min+1)%self.max_size
        self.size_min = self.size_min+1

        while(self.size_max>0 and self.compare_diff_max[(self.end_max-1)%self.max_size][0]<=elem):
            self.end_max = (self.end_max-1)%self.max_size
            self.size_max=self.size_max-1
        self.compare_diff_max[self.end_max]=[elem,self.count]
        self.end_max = (self.end_max+1)%self.max_size
        self.size_max = self.size_max+1

        while(self.compare_diff_min[self.start_min][1]<=self.count-self.days):
            self.start_min = (self.start_min+1)%self.max_size
            self.size_min = self.size_min-1
        while(self.compare_diff_max[self.start_max][1]<=self.count-self.days):
            self.start_max = (self.start_max+1)%self.max_size
            self.size_max = self.size_max-1
        self.min_val = self.compare_diff_min[self.start_min][0]
        self.max_val = self.compare_diff_max[self.start_max][0]

    def get_min(self):
        return self.min_val
    def get_max(self):
        return self.max_val
    

class circular_array_oscillator:
    def __init__(self,look_back_days, days_ema_oscillator=None):
        if(days_ema_oscillator==None):
            days_ema_oscillator = look_back_days
        self.circular_min_max = circular_array_min_max(look_back_days)
        self.look_back_days = look_back_days;
        self.days_ema_oscillator = days_ema_oscillator
        self.ema_stochastic = 0;
        self.stochastic = 0;

    def add_element(self,elem):
        self.circular_min_max.add_element(elem)
        self.stochastic_indicator(elem)
        self.stochastic_ema()


    def stochastic_indicator(self,diff):
        if(self.circular_min_max.get_max()!=self.circular_min_max.get_min()):
            self.stochastic = (diff - self.circular_min_max.get_min())/(self.circular_min_max.get_max()-self.circular_min_max.get_min())
        
    def stochastic_ema(self):
        if(self.circular_min_max.count==1):
            self.ema_stochastic = self.stochastic
        else:
            alpha = 2.0/(1+self.days_ema_oscillator);
            self.ema_stochastic =  self.ema_stochastic*(1-alpha)+alpha*self.stochastic

    def get_stochastic_indicator(self):
        return self.stochastic

    def get_stochastic_ema(self):
        return self.ema_stochastic


class circular_array_ATR:
    def __init__(self,min_max_days,days):
        self.circular_array_max_min = circular_array_min_max(min_max_days)
        self.ATR = 0
        self.days = days
        

    def add_element(self,elem):
        self.circular_array_max_min.add_element(elem)
        self.compute_ATR()
    
    def compute_ATR(self):
        true_range = self.circular_array_max_min.get_max()-self.circular_array_max_min.get_min()
        if(self.circular_array_max_min.count==1):
            self.ATR = true_range
        else:
            alpha = 2.0/(1+self.days)
            self.ATR = (1-alpha)*self.ATR + alpha*true_range

    def get_ATR(self):
        return self.ATR

    def get_min(self):
        return self.circular_array_max_min.get_min()
    
    def get_max(self):
        return self.circular_array_max_min.get_max()
        
    
class circular_array_supertrend:
    def __init__(self,look_back_days,ema_days,multiplier=3):
        self.ATR_class = circular_array_ATR(look_back_days,ema_days)
        self.multiplier = multiplier
    
    def add_element(self,elem):
        self.ATR_class.add_element(elem)
    
    def get_suppertrendupper(self):
        return (self.ATR_class.get_max()+self.ATR_class.get_min())/2 + self.multiplier*self.ATR_class.get_ATR()

    def get_suppertrendlower(self):
        return (self.ATR_class.get_max()+self.ATR_class.get_min())/2 - self.multiplier*self.ATR_class.get_ATR()


class rsi_calculation:
    def __init__(self,days):
        self.days = days
        self.count = 0
        self.rsi = 0
        self.average_gain = 0
        self.average_loss = 0
        self.last_val = 0
    
    def add_element(self,elem):
        self.count = max(self.count+1,self.days)
        if(self.last_val!=0):
            if(elem>self.last_val):
                self.average_gain = (self.average_gain*(self.count-1)+(elem-self.last_val))/self.count
            if(elem<self.last_val):
                self.average_loss = (self.average_loss*(self.count-1)-(elem-self.last_val))/self.count
            #print(self.average_gain)
            #print(self.average_loss)
            self.rsi = 1-1*self.average_loss/(self.average_gain+self.average_loss)
        self.last_val = elem

    def get_rsi(self):
        return self.rsi


class circular_array_slope:
    def __init__(self,num_points,slope_window):
        self.slope_window = slope_window
        self.ema_cal = circular_array_ema_sd(num_points)
        self.arr = []
        for i in range(slope_window):
            self.arr.append(0);
        self.pos = 0
        self.slpoe = 0

    def add_element(self,elem):
        self.ema_cal.add_element(elem)
        elem = self.ema_cal.get_ema()
        self.slpoe = (elem-self.arr[self.pos])/self.slope_window
        self.arr[self.pos] = elem
        self.pos = (self.pos+1)%self.slope_window

    def get_slope(self):
        return self.slpoe
from circular_array import circular_array


class double_top_bottom:


    def __init__(self,look_back_bars) -> None:
        self.MaxRiskPerReward =  30#input(30, step=5, minval=5, maxval=100)
        # self.# DisplayRiskPerReward = input(true)
        self.zigzagvalues = []#array.new_float(0)
        self.zigzagindexes = []#array.new_int(0)
        self.zigzagdir = []#array.new_int(0)
        self.doubleTopBottomValues = []#array.new_float(3)
        self.doubleTopBottomIndexes = []#array.new_int(3)
        self.doubleTopBottomDir = []#array.new_int(3)
        self.last_dir = -1
        self.max_array_size = 10
        self.prev_data = circular_array(look_back_bars)
    # max_bars_back(high, 1000)
    # max_bars_back(low, 1000)
    def highestbars(self, high):
        max_val = self.prev_data.get_max()
        if(max_val == None):
            return 0
        if(max_val < high):
            return 0
        return 100
        # pass # TODO should return number of bars after the high in last 1000 bars

    def lowestbars(self, low):
        # pass # TODO should return number of bars after the low in last 1000 bars
        min_val = self.prev_data.get_min()
        if(min_val == None):
            return 0
        if(min_val > low):
            return 0
        return 100

    def computte_high_low(self):
        return 0, 0
        pass # TODO should return high and low


    # var lineArray = array.new_line(0)
    # var labelArray = array.new_label(0)
    def pivots(self,data):
        high, low = data['high'], data['low']
        ph = None
        if(self.highestbars(high) == 0):
            ph = high
        pl = None
        if(self.lowestbars(low) == 0): 
            pl = low 
        dir = 0
        if(ph and pl==None):
            dir = 1
        else:
            if(pl and ph==None):
                dir = -1
            else:
                dir=self.last_dir
        # dir := iff(ph and na(pl), 1, iff(pl and na(ph), -1, dir[1]))
        return [dir, ph, pl]

    def add_to_array(self, value, index, dir): 
        if(len(self.zigzagvalues) < 2):
            mult = 1 
        else:
            if(dir*value > dir*self.zigzagvalues[1]):
                mult = 2
            else:
                mult = 1
        # (dir*value > dir*array.get(zigzagvalues,1)) ? 2 : 1
        self.zigzagindexes.insert(0, index)
        self.zigzagvalues.insert(0, value)
        self.zigzagdir.insert(0,dir*mult)
        if len(self.zigzagindexes) > self.max_array_size:
            self.zigzagindexes = self.zigzagindexes[:-1]
            zigzagvalues = zigzagvalues[:-1]
            self.zigzagdir = self.zigzagdir[:-1]

    def add_to_zigzag(self, dir, dirchanged, ph, pl, index):
        if(dir == 1):
            value = ph
        else:
            value = pl
        # value = (dir == 1? ph : pl)
        if len(self.zigzagvalues) == 0 or dirchanged:
            self.add_to_array(value, index, dir)
        elif((dir == 1 and value > self.zigzagvalues[0]) or (dir == -1 and value < self.zigzagvalues[0])):
            self.zigzagvalues.pop(0)
            self.zigzagindexes.pop(0)
            self.zigzagdir.pop(0)
            self.add_to_array(value, index, dir)

    def zigzag(self, bar_index, data):
        [dir, ph, pl] = self.pivots(data)
        dirchanged = False
        if(self.last_dir != dir):
            dirchanged = True
        # dirchanged = change(dir)
        if(ph or pl):
            self.add_to_zigzag(dir, dirchanged, ph, pl, bar_index)

    def calculate_double_pattern(self):
        doubleTop = False
        # doubleTopConfirmation = 0
        doubleBottom = False
        # doubleBottomConfirmation = 0
        if(len(self.zigzagvalues) >= 4): 
            index = self.zigzagindexes[1]
            value = self.zigzagvalues[1]
            highLow = self.zigzagdir[1]
            
            lindex = self.zigzagindexes[2]
            lvalue = self.zigzagvalues[2]
            lhighLow = self.zigzagdir[2]
            
            llindex = self.zigzagindexes[3]
            llvalue = self.zigzagvalues[3]
            llhighLow = self.zigzagdir[3]
            risk = abs(value-llvalue)
            reward = abs(value-lvalue)
            riskPerReward = risk*100/(risk+reward)
            
            if(highLow == 1 and llhighLow == 2 and lhighLow < 0  and riskPerReward < self.MaxRiskPerReward):
                doubleTop = True
            if(highLow == -1 and llhighLow == -2 and lhighLow > 0 and riskPerReward < self.MaxRiskPerReward):
                doubleBottom = True

            # if(doubleTop or doubleBottom):
            #     doubleTopBottomValues[0] = value
            #     doubleTopBottomValues[1] = lvalue
            #     doubleTopBottomValues[2] = llvalue
                
            #     doubleTopBottomIndexes[0] = index
            #     doubleTopBottomIndexes[1] = lindex
            #     doubleTopBottomIndexes[2] = llindex
                
            #     doubleTopBottomDir[0] = highLow
            #     doubleTopBottomDir[1] = lhighLow
            #     doubleTopBottomDir[2] = llhighLow
        
        return [doubleTop, doubleBottom]

    # get_crossover_info(doubleTop, doubleBottom)=>
    #     index = array.get(doubleTopBottomIndexes, 0)
    #     value = array.get(doubleTopBottomValues, 0)
    #     highLow = array.get(doubleTopBottomDir, 0)
        
    #     lindex = array.get(doubleTopBottomIndexes, 1)
    #     lvalue = array.get(doubleTopBottomValues, 1)
    #     lhighLow = array.get(doubleTopBottomDir, 1)
        
    #     llindex = array.get(doubleTopBottomIndexes, 2)
    #     llvalue = array.get(doubleTopBottomValues, 2)
    #     llhighLow = array.get(doubleTopBottomDir, 2)
        
    #     latestDoubleTop = false
    #     latestDoubleBottom = false
    #     latestDoubleTop := doubleTop ? true : doubleBottom? false : latestDoubleTop[1]
    #     latestDoubleBottom := doubleBottom? true : doubleTop? false : latestDoubleBottom[1]
        
    #     doubleTopConfirmation = 0
    #     doubleBottomConfirmation = 0
    #     doubleTopConfirmation := latestDoubleTop? (crossunder(low, lvalue) ? 1 : crossover(high, llvalue) ? -1 : 0) : 0
    #     doubleBottomConfirmation := latestDoubleBottom? (crossover(high, lvalue) ? 1 : crossunder(low, llvalue) ? -1 : 0) : 0
    #     [doubleTopConfirmation, doubleBottomConfirmation]
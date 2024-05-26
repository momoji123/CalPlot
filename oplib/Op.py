class Operation:
    def __init__(self, innerOp, parent, is_open):
        self.is_open = is_open
        self.innerOp = innerOp
        self.val = []
        self.parent = parent
    
    def add_val(self, value):
        if value in ['sin', 'cos', 'tan', 'log']:
            childOp = Operation(value, self, True)
            self.val.append(childOp)
            return childOp
        if value == '(':
            self.val.append(str(value))
            childOp = Operation(None, self, True)
            self.val.append(childOp)
            return childOp
        if value == ')':
            if self.parent is not None:
                self.is_open = False
                return self.parent
            else:
                return self
        else:
            self.val.append(str(value))
        return self
    
    def remove_val(self):
        if(len(self.val)<1):
            return self
        
        last_val = self.val[len(self.val)-1]
        if isinstance(last_val, str):
            self.val.pop(len(self.val)-1)
        else:
            if len(last_val.val)==0:
                #child op has no val anymore, then remove it from val list
                self.val.pop(len(self.val)-1)
            else:
                #when still has value in it, then remove last value in it
                return last_val.remove_val()
        return self
    
    def clear(self):
        self.val = []
    
    def get_parent(self):
        return self.parent
        
    def get_eval_str(self, trigon_mode):
        result = ""
        if self.innerOp in ['sin', 'cos', 'tan']:
            result = result + "math." + self.innerOp + "("
            if trigon_mode == "Deg":
                result = result + "math.radians("
        elif self.innerOp in ['log']:
            result = result + "math." + self.innerOp + "("
            
        for value in self.val:
            if isinstance(value, str):
                if value == '^':
                    result = result + "**"
                elif value == 'e':
                    result = result + "math.e"
                else:
                    result = result + value
            else:
                result = result + value.get_eval_str(trigon_mode)
        
        if not self.is_open and self.innerOp != "main":
            if self.innerOp in ['sin', 'cos', 'tan'] and trigon_mode == "Deg":
                result = result + "))"
            else:
                result = result + ")"
        return result
    
    def get_display_str(self):
        result = ""
        if self.innerOp in ['sin', 'cos', 'tan', 'log']:
            result = result + self.innerOp + "("
            
        for value in self.val:
            if isinstance(value, str):
                result = result + value
            else:
                result = result + value.get_display_str()
        
        if not self.is_open and self.innerOp != "main":
            result = result + ")"
        return result
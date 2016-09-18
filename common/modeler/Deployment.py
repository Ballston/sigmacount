class Deployment(object):
    
    def __init__(self,**kwargs):
        self.modellist=[]
        for propertyname,value in kwargs.iteritems():
            if propertyname==data:
                self.data=value
            if propertyname==modellist:
                self.modellist=value
            else:
                print 'I dont understand what you are trying to specify'
                
                
    def addmodel(self,model):
        self.modellist.append(model)
        pass
    
    def runsimple(self):
        pass
    
    def runmonte(self):
        pass
    
    
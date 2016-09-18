class ModelClass(object):
    
    def __init__(self, **kwargs):
        self.transfrom=lambda x:x
        self.inversetransform=lambda x:x
        for propertyname,value in kwargs.iteritems():
            if propertyname=='data' :
                #This is expected to be a pandas
                self.data=value
            elif propertyname=='startdate':
                self.startdate=value
            elif propertyname=='enddate':
                self.enddate=value
            elif propertyname=='dependent':
                self.dependent=value
            elif propertyname=='exogenous':
                #List of exogenous variables to be used
                self.exogenous=value
            elif  propertyname=='transform':
                self.transform=value
            elif propertyname=='inversetransform':
                self.inversetransform=value
            else:
                 print('I dont know which property you are trying to define by %s='%(propertyname) )
                 
    
    def setmodel(self,**kwargs):
        import statsmodels.api as sm
        #Set model specification for now ARIMA is the only specification
        self.I=0
        self.AR=0
        self.MA=0
        for propertyname,value in kwargs.iteritems():
            if propertyname=='I':
                self.I=value
            elif propertyname=='AR':
                self.AR=value
            elif propertyname=='MA':
                self.MA=value
            else:
                print 'I dont understand the model specification you are attempting to define'
        
        self.model=sm.tsa.ARIMA(self.transform(self.data[self.dependent][self.startdate:self.enddate]) ,(self.AR, self.I, self.MA), exog=self.data[self.exogenous][self.startdate:self.enddate])
        pass
                    
        
    def estimate(self):
        self.fit=self.model.fit()
        pass
    
    def insample(self):
        self.insample=self.fit.predict( exog=self.data[self.exogenous][self.startdate:self.enddate] )
        pass
        
    def forcast(self):
        pass
    
    def clear(self):
        pass
        




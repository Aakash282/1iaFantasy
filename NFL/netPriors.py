import h2o 
import pandas as pd
import os
h2o.init()


if __name__ == '__main__':
    home = os.getcwd()
    home = home[:-14] + 'fanduel/NFL/'
    dataPath = home + 'computedData.csv'
    df = h2o.import_file(path=dataPath)
    # data = pd.DataFrame.from_csv(home + 'computedData.csv')
	
	
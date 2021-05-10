import os
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

def predictPrices(path):
    r = robjects.r
    sourcepath = os.path.abspath("rpy2/project/R/predict.R")
    source = r.source(sourcepath)
    from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
    project = SignatureTranslatedAnonymousPackage("predictPrice <- " + str(source[0]), "project")
    return project.predictPrice(path)

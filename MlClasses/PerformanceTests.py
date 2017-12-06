from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc
import matplotlib.pyplot as plt
import os
import numpy as np

def classificationReport(clf,X_test,y_test,outputFile=None):
    y_predicted = clf.predict(X_test)
    report = classification_report(y_test, y_predicted,
                                            target_names=["background", "signal"])
    auc= "Area under ROC curve: %.4f"%(roc_auc_score(y_test,clf.decision_function(X_test)))

    if outputFile:
        outputFile.write(report)
        outputFile.write('\n')
        outputFile.write(auc)
    else:
        print report
        print auc
        

def rocCurve(y_preds,y_test=None,output=None,append=''):
    '''Compute the ROC curves, can either pass the predictions and the truth set or 
    pass a dictionary that contains one value 'truth' of the truth set and the other 
    predictions labeled as you want'''

    # Compute ROC curve and area under the curve
    if not isinstance(y_preds,dict):
        assert not y_test is None,'Need to include testing set if not passing dict'
        y_preds={'ROC':y_preds}
    else:
        y_test=y_preds['truth']

    for name,y_pred in y_preds.iteritems():
        if name=='truth': continue
        fpr, tpr, thresholds = roc_curve(y_test, y_pred)
        roc_auc = auc(fpr, tpr)

        plt.plot(fpr, tpr, lw=1, label=name+' (area = %0.2f)'%(roc_auc))

    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.grid()
    if not os.path.exists(output): os.makedirs(output)
    plt.savefig(os.path.join(output,'rocCurve'+append+'.pdf'))
    plt.clf()

def compareTrainTest(clf, X_train, y_train, X_test, y_test, output, bins=30):
    '''Compares the decision function for the train and test BDT'''
    decisions = []
    for X,y in ((X_train, y_train), (X_test, y_test)):
        d1 = clf.decision_function(X[y>0.5]).ravel()
        d2 = clf.decision_function(X[y<0.5]).ravel()
        decisions += [d1, d2]
        
    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)
    
    plt.hist(decisions[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='S (train)')
    plt.hist(decisions[1],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='B (train)')

    hist, bins = np.histogram(decisions[2],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[2]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
    
    hist, bins = np.histogram(decisions[3],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions[3]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

    plt.xlabel("BDT output")
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')
    if not os.path.exists(output): os.makedirs(output)
    plt.savefig(os.path.join(output,'compareTrainTest.pdf'))
    plt.clf()

def plotDiscriminator(clf,X_test,y_test,bins=30):
    plt.hist(clf.decision_function(X_test[y_test==0]).ravel(),color='r', alpha=0.5, bins=bins)
    plt.hist(clf.decision_function(X_test[y_test==1]).ravel(),color='b', alpha=0.5, bins=bins)
    plt.xlabel("scikit-learn classifier output")
    if not os.path.exists(output): os.makedirs(output)
    plt.savefig(os.path.join(output,'discriminator.pdf'))
    plt.clf()


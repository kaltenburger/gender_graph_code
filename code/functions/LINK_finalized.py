from __future__ import division
from sklearn.preprocessing import label_binarize


def LINK(num_unlabeled, membership_y, feature_x, clf, num_iter, cv_setup=None):
    mean_accuracy = []
    se_accuracy = []
    mean_micro_auc = []
    se_micro_auc = []
    mean_wt_auc = []
    se_wt_auc = []
    for i in range(len(num_unlabeled)):
        print num_unlabeled[i]
        if cv_setup=='stratified':
            k_fold = cross_validation.StratifiedShuffleSplit((membership_y), n_iter=num_iter,
                                               test_size=num_unlabeled[i],
                                               random_state=0)
        else:
            k_fold = cross_validation.ShuffleSplit(len(membership_y), n_iter=num_iter,
                                                         test_size=num_unlabeled[i],
                                                         random_state=0)
        accuracy = []
        micro_auc = []
        wt_auc = []
        for k, (train, test) in enumerate(k_fold):
            clf.fit(feature_x[train], np.ravel(membership_y[train]))
            pred = clf.predict(feature_x[test])
            prob = clf.predict_proba(feature_x[test])
            print prob
            print metrics.roc_auc_score(label_binarize(membership_y[test],np.unique(membership_y)),
                                        prob[:,1],average='weighted')
            print metrics.roc_auc_score(label_binarize(membership_y[test],np.unique(membership_y)),
                                                                    prob[:,1]-prob[:,0],average='weighted')
            accuracy.append(metrics.accuracy_score(membership_y[test], pred,  normalize = True))
            
            # auc scores
            if len(np.unique(membership_y))>2:
                micro_auc.append(metrics.roc_auc_score(label_binarize(membership_y[test],np.unique(membership_y)), prob,  average = 'micro'))
                wt_auc.append(metrics.roc_auc_score(label_binarize(membership_y[test],np.unique(membership_y)), prob,
                                                                                                                             average = 'weighted'))
            else:
                micro_auc.append(metrics.roc_auc_score(label_binarize(membership_y[test],np.unique(membership_y)),
                                                                        prob[:,1],average='micro'))
                wt_auc.append(metrics.roc_auc_score(label_binarize(membership_y[test],np.unique(membership_y)),
                                                                            prob[:,1],average='weighted'))
        mean_accuracy.append(np.mean(accuracy))
        se_accuracy.append(np.std(accuracy))
        mean_micro_auc.append(np.mean(micro_auc))
        se_micro_auc.append(np.std(micro_auc))
        mean_wt_auc.append(np.mean(wt_auc))
        se_wt_auc.append(np.std(wt_auc))
    return(mean_accuracy, se_accuracy, mean_micro_auc,se_micro_auc, mean_wt_auc,se_wt_auc)

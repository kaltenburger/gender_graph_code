## 4/24/2017
## about: compute 1-hop, 2-hop MV inference results when 50% of netwokr is labeled

folder_directory = '/Users/kristen/Documents/gender_graph_code/code/functions' # enter local main folder

import os
os.chdir(folder_directory)
execfile('python_libraries.py')
execfile('create_adjacency_matrix.py')
execfile('compute_homophily.py')
execfile('compute_monophily.py')
execfile('parsing.py')  # Sam Way's Code
execfile('mixing.py')   # Sam Way's Code
execfile('majority_vote.py')


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--input-dir', help='Input directory', required=True)
    args.add_argument('-e', '--file-ext', help='Input extension', default='.mat')
    args.add_argument('-o', '--output-dir', help='Output directory', required=True)
    args = args.parse_args()
    return args



if __name__=="__main__":
    args = interface()
    homophily_gender = []
    monophily_gender = []

    
    file_output = open('../../data/facebook_output_majority_vote_class_specific.csv', 'wt')
    j =0
    writer = csv.writer(file_output)
    writer.writerow( ('school', 'percent_initially_unlabeled', '1_MV_F_mean_auc_wt', '1_MV_F_se_auc_wt', '2_MV_F_mean_auc_wt', '2_MV_F_se_auc_wt',
                      '1_MV_M_mean_auc_wt', '1_MV_M_se_auc_wt', '2_MV_M_mean_auc_wt', '2_MV_M_se_auc_wt'))
                      
    percent_initially_unlabelled = [0.5]
    percent_initially_labelled = np.subtract(1, percent_initially_unlabelled)

    for f in listdir(args.input_dir):
        if f.endswith(args.file_ext):
            tag = f.replace(args.file_ext, '')
            j=j+1
            if tag=='Amherst41':
                print "Processing %s..." % tag
                input_file = path_join(args.input_dir, f)
                
                
                ## Descriptive Statistics on Raw, Original Data
                adj_matrix_tmp, metadata = parse_fb100_mat_file(input_file)

                gender_y_tmp = metadata[:,1] #gender
                gender_dict = create_dict(range(len(gender_y_tmp)), gender_y_tmp)
  
                ## Compute Homophily/Monophily on Same Data Object Used for Prediction Setup
                # create corresponding y-/adj- objects
                (gender_y, adj_matrix_gender) = create_adj_membership(nx.from_scipy_sparse_matrix(adj_matrix_tmp),
                                                                      gender_dict,  # gender dictionary
                                                                      0,            # we drop nodes with gender_label = 0, missing
                                                                      'yes',        # yes to removing
                                                                      0,            # set diagonal to 0, ie no self-loops
                                                                      None,         # for an undirected graph - we subset to nodes in largest connected component [ZGL]
                                                                      'gender')
                


                #1-hop MV
                (mean_accuracy_mv, se_accuracy_mv,
                 mean_micro_auc_mv_amherst,se_micro_auc_mv,
                 mean_wt_auc_mv,se_wt_auc_mv) =majority_vote_class_specific(percent_initially_unlabelled,
                                                                                       np.array(gender_y),
                                                                                       np.array(adj_matrix_gender),
                                                                                       num_iter=10)
                                                                                       
                                                                                       
                #2-hop MV
                adj2= np.matrix(adj_matrix_gender)**2
                adj2[range(adj2.shape[0]),range(adj2.shape[0])]=0
    
    
                (mean_accuracy_mv2, se_accuracy_mv2,
                mean_micro_auc_mv2,se_micro_auc_mv2,
                 mean_wt_auc_mv2,se_wt_auc_mv2) =majority_vote_class_specific(percent_initially_unlabelled,
                                                                               np.array(gender_y),
                                                                               np.array(adj2),
                                                                               num_iter=10)
        

                writer.writerow( (tag, percent_initially_labelled[0], mean_wt_auc_mv[0], se_wt_auc_mv[0],mean_wt_auc_mv2[0], se_wt_auc_mv2[0]))

    file_output.close()
    print "Done!"
                

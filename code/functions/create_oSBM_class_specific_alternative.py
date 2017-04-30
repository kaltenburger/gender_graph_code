from __future__ import division

## 12/18/2016
## update: allow class-specific dispersion parameter
## note: assumes dispersion_val_vect is in the same order as the class [class1, class2] --> dispersion_val_vect = [dispersion_val_vect_1, dispersion_val_vect_2]
## simply put, the numeric ordering of the class determines the ordering of the

## final general oSBM model with flexible class sizes -- & defined in terms of \phi, p_in, p_out



def create_proportion_class_k_friends(adj_matrix, node_id,
                                     y_labels, k_class):
    prop_class_k_friends = []
    total_neighbors = []
    total = np.sum(adj_matrix,1)
    class_k_num = adj_matrix*np.matrix((y_labels==k_class)+0).T
    prop_class_k =class_k_num/total
    return(np.array(prop_class_k).T[0])



def create_expected_degree_sequence(class_size_val,#num_classes,
                                    p_in_val, p_out_val,
                                    dispersion_val_in, dispersion_val_out):
    ## in-class
    if(dispersion_val_in != 0):
        alpha_in = p_in_val * (1/dispersion_val_in) * (1-dispersion_val_in)
        beta_in = (1-p_in_val) * (1/dispersion_val_in) * (1-dispersion_val_in)
        #print 'alpha_in: ', alpha_in
        #print 'beta_in: ', beta_in
        #print ''
        p_in_dispersed = np.matrix(np.random.beta(alpha_in, beta_in, size=class_size_val))
        in_class_expected_degree = p_in_dispersed * class_size_val # probability of link * number of possible in-LINKS
    if(dispersion_val_in == 0):
        in_class_expected_degree = np.matrix([class_size_val * p_in_val] * class_size_val)

    ## out-class
    if(dispersion_val_out != 0):
        alpha_out = p_out_val * (1/dispersion_val_out) * (1-dispersion_val_out)
        beta_out = (1-p_out_val) * (1/dispersion_val_out) * (1-dispersion_val_out)
        #print alpha_out
        #print beta_out
        #print ''
        p_out_dispersed = np.matrix(np.random.beta(alpha_out, beta_out, size=class_size_val))
        out_class_expected_degree = p_out_dispersed * class_size_val # probability of link * number of possible out-LINKS
    if(dispersion_val_out == 0):
        out_class_expected_degree = np.matrix([class_size_val * p_out_val] * class_size_val)
    return(in_class_expected_degree, out_class_expected_degree)



def in_class_matrix(matrix):
    return(matrix.T*matrix)

def out_class_matrix(matrix1,matrix2):
    return(matrix1.T*matrix2)



## assumes k=2 class set-up
## p_in = [p_in_1, p_in_2]
def create_affiliation_model_temp(average_node_degree,
                                  lambda_block_parameter,
                                  dispersion_parameter_vect,
                                  class_size_vect):#, num_classes):
    
    #N = class_size * num_classes #total number of nodes in graph
    N = np.sum(class_size_vect)
    
    ### BLOCK STRUCTURE
    ## define p_in; p_out
    p_in = (lambda_block_parameter * average_node_degree)/N
    print 'p_in: ', p_in
    
    #previous parameterization
    #p_out = (average_node_degree - p_in * class_size)/((num_classes-1)*class_size)
    denominator = []
    for j in range(len(class_size_vect)):
        denominator.append(class_size_vect[j] * class_size_vect[~j])
    denom = np.sum(denominator)
    p_out = (average_node_degree * N - np.sum(class_size_vect**2 * p_in))/denom
    print 'p_out: ', p_out
    print ''

    ## Expected Degree Sequence for nodes in class 1,2,...k
    ## Generates in-class degree sequence and out-class sequence
    in_class_list = []
    out_class_list = []
    for j in range(len(class_size_vect)):
        #intent here is to iterate through each class
        #and important -- assumes a specific data format for input dispersion_parameter_vect
        (in_class, out_class) = create_expected_degree_sequence(class_size_vect[j],p_in,p_out,dispersion_parameter_vect[j][0], dispersion_parameter_vect[j][1])
        in_class_list.append(in_class)
        out_class_list.append(out_class)


    ## testing only
    #r_same = ro.r.array(np.array(map(np.round, np.array(in_class_list[0])[0])))#, nrow=nr, ncol=nc)
    #ro.r.assign("r_same", r_same)
    #r_diff = ro.r.array(np.array(map(np.round, np.array(out_class_list[0])[0])))#, nrow=nr, ncol=nc)
    #ro.r.assign("r_diff", r_diff)
    
    #print 'Williams monophily: ', ( np.float(np.array(r_f(r_same, r_diff))[0]))
    #print ''

    #print 'compare dispersions in d_i,same, d_i,diff, d_i,same/d_i: '
    #print np.std(np.array(map(np.round, np.array(in_class_list[0])[0])))
    #print np.std(np.array(map(np.round, np.array(out_class_list[0])[0])))
    #print np.std(np.array(map(np.round, np.array(in_class_list[0])[0])) + np.array(map(np.round, np.array(out_class_list[0])[0])))
    #print ''
    #print np.mean(np.array(map(np.round, np.array(in_class_list[0])[0]))/(np.array(map(np.round, #np.array(in_class_list[0])[0] + np.array(out_class_list[0])[0]))))
    #print ( np.std(np.array(map(np.round, np.array(in_class_list[0])[0]))/(np.array(map(np.round, np.array(in_class_list[0])[0] + np.array(out_class_list[0])[0])))))
    #print ''


    expected_prob_matrix=np.zeros((N,N))
    for i in range(len(class_size_vect)):
        for j in range(len(class_size_vect)):
            idx = np.sum(class_size_vect[0:i])#i * class_size_vect[j] #row
            jdx = np.sum(class_size_vect[0:j])# j * class_size_vect[j] #column
            #print expected_prob_matrix
            if i==j:
                expected_prob_matrix[idx:idx+class_size_vect[j],jdx:jdx+class_size_vect[j]] = in_class_matrix(in_class_list[j])/(class_size_vect[j]**2*p_in)
                #print expected_prob_matrix
                #print ''
            else:
                out = out_class_matrix(out_class_list[i], out_class_list[j])/(class_size_vect[i]*class_size_vect[j]*p_out)
                #print out_class_list[i].T
                #print out
                if j<i:
                    #print np.shape(expected_prob_matrix[idx:idx+class_size_vect[i],jdx:jdx+class_size_vect[j]] )
                    #print out
                    expected_prob_matrix[idx:idx+class_size_vect[i],jdx:jdx+class_size_vect[j]] = out
                    #print expected_prob_matrix
                    #print ''
                if i<j:
                    expected_prob_matrix[idx:idx+class_size_vect[i],jdx:jdx+class_size_vect[j]] = out
                    #print expected_prob_matrix
                    #print ''
    #print expected_prob_matrix

    #print 'expected_prob_matrix:'
    #print expected_prob_matrix
    A_ij_tmp = np.matrix(map(bernoulli.rvs,expected_prob_matrix))
    Adj_corrected = np.matrix(np.triu(A_ij_tmp, k=0) + np.transpose(np.triu(A_ij_tmp, k=1)))
    #print type(np.matrix(Adj_corrected))
    #Membership = np.sort(np.tile(np.array(range(num_classes)), class_size))
    Membership = np.concatenate(map(np.tile,np.array(range(len(class_size_vect))), class_size_vect),0)
    #print Membership
    #print ''
    #print 'Spot-checks:'
    #print 'spot-check t(Adj)=Adj'
    #print np.sum(np.matrix(Adj_corrected) != np.transpose(np.matrix(Adj_corrected)))
    #print ''

    print 'spot-check average degree: '
    print np.mean(np.sum(np.matrix(Adj_corrected), axis=1))
    print ''

    print 'spot-check homophily: '
    print homophily_index_Jackson_alternative(np.matrix(Adj_corrected), np.array(Membership))
    print ''

    print 'spot-check monophily: '
    print monophily_index_overdispersion_Williams(np.matrix(Adj_corrected), np.array(Membership))
    #result = monophily_index_overdispersion_Williams(np.matrix(Adj_corrected), np.array(Membership))
    #print type(result)
    #return( (result [0] > result[1])+0)
    print ''
    return( Adj_corrected, Membership)








### old code below -- some of the code below might be useful for creating histograms/formatting

#def create_affiliation_model(average_node_degree,
#                             lambda_block_parameter,
#                             dispersion_parameter_vect,
#                             class_size, num_classes):
#
#    N = class_size * num_classes #total number of nodes in graph
#
#    ### BLOCK STRUCTURE
#    ## define p_in; p_out
#    p_in = (lambda_block_parameter * average_node_degree)/N
#    #print p_in
#    p_out = (average_node_degree - p_in * class_size)/((num_classes-1)*class_size)
#    #print p_out
#
#    ## Expected Degree Sequence for nodes in class 1,2,...k
#    ## Generates in-class degree sequence and out-class sequence
#    in_class_list = []
#    out_class_list = []
#    for j in range(num_classes):
#        (in_class, out_class) = create_expected_degree_sequence(class_size,num_classes,p_in,p_out,dispersion_parameter_vect)
#        in_class_list.append(in_class)
#        out_class_list.append(out_class)
#
#    expected_prob_matrix=np.zeros((N,N))
#    for i in range(num_classes):
#        for j in range(num_classes):
#            idx = i * class_size #row
#            jdx = j * class_size #column
#            if i==j:
#                expected_prob_matrix[idx:idx+class_size,jdx:jdx+class_size] = in_class_matrix(in_class_list[i])/(class_size**2*p_in)
#            else:
#                out = out_class_matrix(out_class_list[i], out_class_list[j])/(class_size**2*p_out)
#                if j<i:
#                    expected_prob_matrix[idx:idx+class_size,jdx:jdx+class_size] = out
#                if i<j:
#                    expected_prob_matrix[idx:idx+class_size,jdx:jdx+class_size] = out.T
#    #print 'expected_prob_matrix:'
#    #print expected_prob_matrix
#    A_ij_tmp = np.matrix(map(bernoulli.rvs,expected_prob_matrix))
#    Adj_corrected = np.matrix(np.triu(A_ij_tmp, k=0) + np.transpose(np.triu(A_ij_tmp, k=1)))
#    #print type(Adj_corrected)
#    Membership = np.sort(np.tile(np.array(range(num_classes)), class_size))
#
#
#    #print 'Spot-checks:'
#    #print 'spot-check t(Adj)=Adj'
#    #print np.sum(Adj_corrected != np.transpose(Adj_corrected))
#                                                                       
#    #print 'spot-check average degree: '
#    #print np.mean(np.sum(Adj_corrected, axis=1))
#    #print ''
#
#    #print 'spot-check average degree: '
#    #    for i in range(len(np.unique(Membership))):
#    #        print np.mean(np.sum(Adj_corrected[Membership==np.unique(Membership)[i]], axis=1))
#    #    print ''
#        
#                                                                           
#    ### SPOT-CHECK on assortativity -- can delete later
#    ## Determine assortativity
#    G_dcsbm = nx.to_networkx_graph(Adj_corrected)
#    node_id,degrees=zip(*G_dcsbm.degree().items())
#    attribute_dict_dispersed = create_dict(node_id, Membership)
#    nx.set_node_attributes(G_dcsbm, 'attribute', attribute_dict_dispersed)
#    #print 'assortativity: '
#    #print nx.attribute_assortativity_coefficient(G_dcsbm, 'attribute')
#    #print ''
#
## old - previously printing graphs
##    tmp = np.copy(np.array(Membership))
##    np.random.shuffle(tmp)
##   
##
#
#
##    for j in np.unique(Membership):
##        binBoundaries = 40
##        f,  axarr = plt.subplots(figsize=(8,5))
##
##        axarr.hist( np.array(np.sum(Adj_corrected,1))[np.array(Membership)==j],
##                                                                           bins=binBoundaries,
##                                                                           alpha = 0.3, label='empirical',
##                                                                           edgecolor = 'white', color='red')
##        for n in np.unique(Membership):
##            if n != j:
##                axarr.hist( np.array(np.sum(Adj_corrected,1))[np.array(Membership)==n],
##                                                                           bins=binBoundaries,
##                                                                           alpha = 0.3, label='empirical',
##                                                                           edgecolor = 'white')
##
##        plt.title('Class: '+str(j))
##        plt.show()
#
#
#
##    for j in np.unique(Membership):
##        print j
##        observed_proportion = create_proportion_class_k_friends(Adj_corrected,
##                                                            node_id,
##                                                                Membership,j)
##        shuffled_proportion = create_proportion_class_k_friends(Adj_corrected,
##                                                                node_id,
##                                                                tmp,j)
##
##        binBoundaries = 60
##        f,  axarr = plt.subplots(figsize=(8,5))
##        axarr.hist( np.array(shuffled_proportion)[np.array(tmp)==j],
##                  bins=binBoundaries, 
##                  alpha = 1, label='shuffle',
##                  range = (0,1),edgecolor = 'red', color='white',histtype='step')
##        axarr.hist( np.array(observed_proportion)[np.array(Membership)==j],
##                             bins=binBoundaries,
##                             alpha = 0.3, label='empirical',
##                             range = (0,1),edgecolor = 'white', color='red')
##                  
##        for n in np.unique(Membership):
##            if n != j:
##                axarr.hist( np.array(shuffled_proportion)[np.array(tmp)==n],
##                             bins=binBoundaries,
##                             alpha = 1, label='shuffle',
##                             range = (0,1),edgecolor = 'blue', color='white',histtype='step')
##
##                axarr.hist( np.array(observed_proportion)[np.array(Membership)==n],
##                   bins=binBoundaries,
##                   alpha = 0.3, label='empirical',
##                   range = (0,1),edgecolor = 'white', color='blue')
##        plt.annotate('class k', xy=(0.8, 25),
##                                color='red', alpha=0.5, size=9)
##        plt.annotate('!class k', xy=(0.8, 20),
##                            color='blue', alpha=0.5, size=9)
##        f.text(0.5, 0.04, 'Proportion of Class k Friends', ha='center')
##        f.text(0.04, 0.5, 'Frequency of Ego Nodes', va='center', rotation='vertical')
##        plt.title('Class: '+str(j))
##        plt.show()
#    return(p_in, p_out, Adj_corrected, Membership)

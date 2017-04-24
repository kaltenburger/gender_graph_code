from __future__ import division

## 4/24/2017
## about: process homophily/monophily across all Add Health Schools [in-directed]


## for reference: [Male == 1; Female == 2, Unreported/Missing = 0]
## codings are based on: http://moreno.ss.uci.edu/data.html#adhealth

## run: cd [file path for code]; python add_health_script_homophily_monophily_directed_in.py -i='FILE PATH FOR converted_gml' -o='output path'
folder_directory = '/Users/kristen/Documents/gender_graph_code/code/functions' # enter main folder directory

import os
os.chdir(folder_directory)
execfile('python_libraries.py')
execfile('compute_homophily.py')
execfile('compute_monophily.py')
execfile('compute_chi_square.py')
execfile('parsing.py')  # Sam Way's Code
execfile('mixing.py')   # Sam Way's Code
execfile('create_directed_adjacency_matrix.py')

def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--input-dir', help='Input directory', required=True)
    args.add_argument('-e', '--file-ext', help='Input extension', default='.gml') # KM - files already converted to .gml - find this code
    args.add_argument('-o', '--output-dir', help='Output directory', required=True)
    args = args.parse_args()
    return args



if __name__=="__main__":
    args = interface()
    homophily_gender = []
    monophily_gender = []

    
    file_output = open('../pnas_output_data/add_health_output_in_directed_links_homophily_monophily.csv', 'wt') # change file name to directed
    j =0
    writer = csv.writer(file_output)
    writer.writerow( ('school', 'raw_F_count', 'raw_M_count', 'raw_?_count',
                      'cc_F_count', 'cc_M_count', 'ratio_F',
                      'cc_average_degree_F', 'cc_average_degree_M','cc_max_deg_F','cc_max_deg_M',
                      'cc_homophily_F', 'cc_homophily_M',
                      'cc_homophily_p_value_glm_F','cc_homophily_p_value_glm_M',
                      'cc_homophily_p_value_dispmod_glm_F','cc_homophily_p_value_dispmod_glm_M',
                      'b0_glm_F','b0_dispmod_glm_F', 'b0_glm_M','b0_dispmod_glm_M',
                      'cc_monophily_F', 'cc_monophily_M',
                      'chi_square_p_value_F', 'chi_square_p_value_M'))

                      
    os.chdir('/Users/kristen/Dropbox/gender_graph_data/add-health/converted_gml/') ## replace with file path to converted_gml
    for f in listdir(args.input_dir):
        if f.endswith(args.file_ext):
            tag = f.replace(args.file_ext, '')
            j=j+1

            id = re.findall(r'\d+', f)
            print "Processing %s..." % f

            # updated for directed version of graph
            ah_graph = nx.read_gml(f)
 
 
            #out-link
            (ah_gender_in, adj_gender_in) = create_directed_adj_membership(ah_graph,
                                                                nx.get_node_attributes(ah_graph, 'comm' + str(id[0]) +'sex'), ## fix for non-mutual links here
                                                                   0,
                                                                   'yes',
                                                                   0,
                                                                   'in', # change adjacency matrix type: out == out-link, in == in-link, any1 == undirected
                                                                   'gender')
        

            ## Descriptive Statistics on Raw, Original Data
            gender_y_tmp = nx.get_node_attributes(ah_graph, 'comm' + str(id[0]) +'sex')
            
            # Original Data
            raw_gender_F_undirected = np.sum((np.array(gender_y_tmp.values())==2)+0)
            raw_gender_M_undirected = np.sum((np.array(gender_y_tmp.values())==1)+0)
            raw_gender_unknown_undirected = np.sum((np.array(gender_y_tmp.values())==0)+0)

            
            # gender-/class-year relative proportions
            proportion_gender = []
            block_size_gender = []
            avg_deg_gender = []
            max_deg = []
            class_labels = np.sort(np.unique(np.array(ah_gender_in)))
            for i in range(len(class_labels)):
                block_size_gender.append( np.sum((ah_gender_in==class_labels[i])+0))
                proportion_gender.append( np.mean(ah_gender_in==class_labels[i]))
                avg_deg_gender.append(np.mean(np.array(np.sum(adj_gender_in,1))[ah_gender_in==class_labels[i]]))
                max_deg.append(np.max(np.array(np.sum(adj_gender_in,1))[ah_gender_in==class_labels[i]]))
            proportion_gender = np.array(proportion_gender)
            avg_deg_gender = np.array(avg_deg_gender)
            block_size_gender = np.array(block_size_gender)
            max_deg = np.array(max_deg)


            if len(block_size_gender) >= 2:
                ## AH - homophily
                ## 12/30 - here -- confirm how homophily is being computed on in-degrees
                homophily_gender =  homophily_index_Jackson_alternative(adj_gender_in, ah_gender_in) # observed homophily
                obs_homophily_F = homophily_gender[1]   # F - important assumes F label < M label
                obs_homophily_M = homophily_gender[0] # M - important assumes M label > F label
                
                homophily_significance = monophily_index_overdispersion_Williams_with_intercept_SE(adj_gender_in, ah_gender_in)
                cc_homophily_p_value_F_glm = homophily_significance[:,1][0]
                cc_homophily_p_value_F_glm_dispmod = homophily_significance[:,1][1]
                
                cc_homophily_p_value_M_glm = homophily_significance[:,0][0]
                cc_homophily_p_value_M_glm_dispmod = homophily_significance[:,0][1]


                ## compare with b0 terms
                b0_temp = np.exp(monophily_index_overdispersion_Williams_with_intercept(np.matrix(adj_gender_in), np.array(ah_gender_in)))
                b0_glm_F = (b0_temp/(1+b0_temp))[:,1][0] # F
                b0_glm_M = (b0_temp/(1+b0_temp))[:,0][0] # M
                
                b0_dispmod_glm_F = (b0_temp/(1+b0_temp))[:,1][1] # F
                b0_dispmod_glm_M = (b0_temp/(1+b0_temp))[:,0][1] # M
                
                
                ## AH - monophily
                monophily_gender = monophily_index_overdispersion_Williams(adj_gender_in, ah_gender_in)
                obs_monophily_F = np.float(monophily_gender[1])  # F - important assumes F label < M label
                obs_monophily_M = np.float(monophily_gender[0]) # M - important assumes M label > F label
                
                chi_square_p_value_gender = compute_chi_square_statistic(np.matrix(adj_gender_in), np.array(ah_gender_in))
                chi_square_p_value_F = np.float(chi_square_p_value_gender[1])
                chi_square_p_value_M = np.float(chi_square_p_value_gender[0])
                

                
                block_F =block_size_gender[1]
                block_M =block_size_gender[0]
                avg_deg_F = avg_deg_gender[1]
                avg_deg_M = avg_deg_gender[0]
                max_deg_F = max_deg[1]
                max_deg_M = max_deg[0]
                prop_F =block_F/(block_F+block_M)
            else:
                ## AH - homophily
                homophily_gender =  ''
                obs_homophily_F = ''
                obs_homophily_M = ''
                
                b0_glm_F = ''
                b0_dispmod_glm_F= ''
                b0_glm_M= ''
                b0_dispmod_glm_M= ''
                
                ## AH - monophily
                monophily_gender = ''
                obs_monophily_F = ''
                obs_monophily_M = ''
                block_F =''
                block_M =''
                avg_deg_F = ''
                avg_deg_M = ''
                prop_F = ''
                chi_square_p_value_F= ''
                chi_square_p_value_M = ''
                cc_homophily_p_value_F_glm = ''
                cc_homophily_p_value_M_glm = ''
                cc_homophily_p_value_F_glm_dispmod = ''
                cc_homophily_p_value_M_glm_dispmod = ''

            writer.writerow( (tag, raw_gender_F_undirected,raw_gender_M_undirected, raw_gender_unknown_undirected,
                  block_F, block_M,prop_F,
                  avg_deg_F, avg_deg_M,max_deg_F,max_deg_M,
                  obs_homophily_F, obs_homophily_M,
                cc_homophily_p_value_F_glm,cc_homophily_p_value_M_glm,
                    cc_homophily_p_value_F_glm_dispmod, cc_homophily_p_value_M_glm_dispmod,
                  b0_glm_F,b0_dispmod_glm_F, b0_glm_M, b0_dispmod_glm_M,
                  obs_monophily_F,obs_monophily_M,
                  chi_square_p_value_F, chi_square_p_value_M))


    file_output.close()
    print "Done!"

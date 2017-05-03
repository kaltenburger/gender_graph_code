## about: convert original Add Health CD Data from .paj format --> .gml format

rm(list=ls())

## note: user sets path to file location of raw add health data
file_path_to_raw_add_health_data <-"/Users/kristen/Dropbox/gender_graph_data/add-health/cd_data/structure_nocontract/"


setwd(file_path_to_raw_add_health_data)

library(intergraph)
library(network)


for(files in list.files()){
  print(files)
  file_num <- as.numeric(gsub(".paj","",gsub("comm", "", files))) ## get file name number
  library(network)
  comm <- read.paj(files) ## read in file

  ## first get node attributes
  attributes <- c(names(comm$partitions)) # get names of all possible attributes which may vary

  # create data frame of vertex id + attributes
  attribute_df <- data.frame("vertex.names" =( c(get.vertex.attribute(comm$networks[[1]], 
                                                                      'vertex.names'))))
  ## check for duplicate node IDs
  if(anyDuplicated(c(as.integer( c(get.vertex.attribute(comm$networks[[1]], 'vertex.names'))))) > 0){
    print('error: duplicated node IDs')
  }

  num <- nrow(attribute_df)
  for(i in 1:length(attributes)){
    if(length(c(comm$partitions[i])[[1]]) != num){
      print('mismatch length error')
    }
    # note: implicitly assuming order of attributes corresponds with node id order
    attribute_df[,attributes[i]] <- c(comm$partitions[i])
  }
  ## kristen - 7/27/2016 - spot-checked comm1 attribute aligns with raw file
  ## refs: https://cran.r-project.org/web/packages/intergraph/vignettes/howto.html 
  ## in particular the "Handling attributes" section since igraph/network store them differently
  
  library(network)
  library(intergraph)
  
  g <- asIgraph(comm$networks[[1]])
  library(intergraph)
  detach("package:intergraph", unload=TRUE)
  detach("package:network", unload=TRUE)
  library(igraph)

  ## attach node attribute data.frame to graph object g
  for(j in 1:length(attributes)){
    g <- set.vertex.attribute(g, 
                  name = attributes[j],
                  value=c(attribute_df[,c(attributes[j])]))
  }
  
  write.graph(g, file = paste0('../../converted_gml/', gsub(".paj", ".gml", files)),format = c('gml')) ## user sets path to location of converted files
  detach("package:igraph", unload=TRUE)
}

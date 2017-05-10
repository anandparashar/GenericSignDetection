'''
Created on May 7, 2017

@author: Erich O'Saben
'''


import pandas as pd
import numpy as np
import os
import sys
import utils as u



def main(version, is_gray_only):

    true_df = pd.read_csv(u.ALL_ANNOTATIONS, sep=';')

    
    dir_search_string = "aiua120214-1/|aiua120214-2/|aiua120306-0/|aiua120306-1/"
    if not is_gray_only:
        dir_search_string = "vid8/|vid9/|vid10/|vid11/|" + dir_search_string
    
    
    
    filtered_df = true_df[true_df.Filename.str.contains("vid8/|vid9/|vid10/|vid11/|aiua120214-0/|aiua120214-1/|aiua120214-2/|aiua120306-0/|aiua120306-1/" )]
    
    neg_df = pd.read_csv(os.path.join(u.NEGATIVES_PATH, "../negatives.dat"))
    neg_df.columns = ["Filename"]
    
    neg_df["Filename"] = neg_df.apply(lambda x: os.path.join("negatives",x["Filename"]), axis=1)
    
    unique_files = pd.unique(filtered_df.Filename.values)
    
    
    #need to sample the files to make sure that every annotation for the file are in the Ground Truth File
    #If not, the FN rate will be inflated because a shape found in the image might not have been sampled from Annotations file.     
    file_sample = np.random.choice(unique_files, (430)).tolist()
    
    
    true_samples_df = filtered_df[filtered_df.Filename.isin(file_sample)]
    neg_samples_df = neg_df.sample(len(true_samples_df))
    
        
    final_df = pd.concat([true_samples_df,neg_samples_df])
    final_df = final_df.reindex(columns=true_df.columns)
    
    file_sample += neg_samples_df.Filename.values.tolist()
    print "number of true samples:", len(true_samples_df)
        
    print "final number of samples", final_df.shape[0]
    
    final_df.to_csv(os.path.join("..", "test_data", "testGroundTruth{}.csv".format(version)),index=0, sep=";", header=0)
    pd.DataFrame(data=file_sample).to_csv(os.path.join("..", "test_data", "testGroundTruthFileNames{}.txt".format(version)), header=0, index=0)
   
    

if __name__ == '__main__':
    
    is_gray_only = False
    if len(sys.argv) < 2:
        print "USAGE: Add the version number for the data set you want to create. Optional, add -g if you want a test set with only gray images"
    
    if len(sys.argv) == 3:
        if sys.argv[2] == "-g":
            is_gray_only = True
    
    version = sys.argv[1]
 
    
    main(version, is_gray_only)
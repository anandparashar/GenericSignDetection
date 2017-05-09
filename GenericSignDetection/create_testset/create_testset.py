'''
Created on May 7, 2017

@author: Erich O'Saben
'''

import utils as u
import pandas as pd
import numpy as np
import os
import sys


def main():

    true_df = pd.read_csv(u.ALL_ANNOTATIONS, sep=';')

    #print true_df.shape
    
    filtered_df = true_df[true_df.Filename.str.contains("vid8/|vid9/|vid10/|vid11/|aiua120214-0/|aiua120214-1/|aiua120214-2/|aiua120306-0/|aiua120306-1/" )]
    
    print filtered_df.shape
    #print filtered_df.head()
    
    #sys.exit()
    
    neg_df = pd.read_csv(os.path.join(u.NEGATIVES_PATH, "../negatives.dat"))
    neg_df.columns = ["Filename"]
    
    neg_df["Filename"] = neg_df.apply(lambda x: os.path.join("negatives",x["Filename"]), axis=1)
    
    #print neg_df.head()
    #sys.exit()
    
    unique_files = pd.unique(filtered_df.Filename.values)
    
    #print unique_files
    
    
    #need to sample the files to make sure that every annotation for the file are in the Ground Truth File
    #If not, the FN rate will be inflated because a shape found in the image might not have been sampled from Annotations file.     
    file_sample = np.random.choice(unique_files, (430)).tolist()
    
    
    true_samples_df = filtered_df[filtered_df.Filename.isin(file_sample)]
        
    neg_samples_df = neg_df.sample(len(true_samples_df))
    
    #print neg_samples_df.shape
    
    final_df = pd.concat([true_samples_df,neg_samples_df])
    
    final_df = final_df.reindex(columns=true_df.columns)
    
    file_sample += neg_samples_df.Filename.values.tolist()
    print "number of true samples:", len(true_samples_df)
    
    
    
    print "final number of samples", final_df.shape[0]
    #print final_df.head()
    
    #print final_df.columns
    
    final_df.to_csv("testGroundTruth2.csv",index=0, sep=";", header=0)
    pd.DataFrame(data=file_sample).to_csv("testGroundTruthFileName2.txt", header=0, index=0)
   
    

if __name__ == '__main__':
    main()
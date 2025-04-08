import pandas as pd
import random
import os
 
# Path to your existing manifest
manifest_path = "filelists/ArVoice_prepared_final_SR_predicted.txt"
output_dir = "filelists/"
 
# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
 
# Read the manifest file
df = pd.read_csv(manifest_path, sep='|', header=None)
df.columns = ['filepath', 'speaker_id', 'text']
 
# Get count by speaker
speaker_counts = df['speaker_id'].value_counts()
max_count = speaker_counts.max()
 
# Create balanced dataset by duplicating entries
balanced_dfs = []
for speaker_id in speaker_counts.index:
    speaker_df = df[df['speaker_id'] == speaker_id]
    # If this speaker has fewer samples than the maximum, duplicate some
    if len(speaker_df) < max_count:
        # How many more samples we need
        num_to_add = max_count - len(speaker_df)
        # Randomly sample with replacement
        additional_samples = speaker_df.sample(n=num_to_add, replace=True, random_state=42)
        speaker_df = pd.concat([speaker_df, additional_samples])
    balanced_dfs.append(speaker_df)
 
# Combine all speakers' data
balanced_df = pd.concat(balanced_dfs)
 
# Shuffle the data
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
 
# Split into train (90%) and validation (10%)
train_size = int(len(balanced_df) * 0.9)
train_df = balanced_df[:train_size]
val_df = balanced_df[train_size:]
 
# Write to files
train_df.to_csv(os.path.join(output_dir, "arvoice_train_filelist.txt"), sep='|', header=False, index=False)
val_df.to_csv(os.path.join(output_dir, "arvoice_val_filelist.txt"), sep='|', header=False, index=False)
 
print(f"Created manifest files:")
print(f"Training set: {len(train_df)} entries")
print(f"Validation set: {len(val_df)} entries")
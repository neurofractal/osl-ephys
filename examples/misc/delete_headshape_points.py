'''
Typically, you would do this function after running source_recon.rhino.coreg 
(either directly, or via the batch API), and after diagnosing a bad coreg 
(again, either directly using source_recon.rhino.coreg_display , or via the html 
report generated by using the batch API).
'''

## Download files
!pip install osfclient

import os
import os.path as op
from osl import utils
from osl.source_recon.rhino import polhemus
from osl import source_recon
import numpy as np

'''
To put ourselves in this situation we will first download the appropriate data 
and copy the headshape points to the appropriate paths in the assumed RHINO 
directory structure:
'''

def get_data(name):
    print('Data will be in directory {}'.format(os.getcwd()))
    """Download a dataset from OSF."""
    if os.path.exists(f"{name}"):
        return f"{name} already downloaded. Skipping.."
    os.system(f"osf -p zxb6c fetch SourceRecon/data/{name}.zip")
    os.system(f"unzip -o {name}.zip")
    os.remove(f"{name}.zip")
    return f"Data downloaded to: {name}"

# Download the dataset
get_data("notts_2subjects")

## Setup file names
data_dir = './notts_2subjects'
recon_dir = './notts_2subjects/recon'

subject = '{subject}'
fif_files_path = op.join(data_dir, subject, subject + '_task-resteyesopen_meg_preproc_raw.fif')    
fif_files = utils.Study(fif_files_path)
subjects = fif_files.fields['subject']
fif_files = fif_files.get()

## Copy polhemus files
def copy_polhemus_files(recon_dir, subject, preproc_file, smri_file, logger):
    polhemus_headshape = np.loadtxt(op.join(data_dir, subject, 'polhemus/polhemus_headshape.txt'))
    polhemus_nasion = np.loadtxt(op.join(data_dir, subject, 'polhemus/polhemus_nasion.txt'))
    polhemus_rpa = np.loadtxt(op.join(data_dir, subject, 'polhemus/polhemus_rpa.txt'))
    polhemus_lpa = np.loadtxt(op.join(data_dir, subject, 'polhemus/polhemus_lpa.txt'))
    
    #  Get coreg filenames
    filenames = source_recon.rhino.get_coreg_filenames(recon_dir, subject)

    # Save
    np.savetxt(filenames["polhemus_nasion_file"], polhemus_nasion)
    np.savetxt(filenames["polhemus_rpa_file"], polhemus_rpa)
    np.savetxt(filenames["polhemus_lpa_file"], polhemus_lpa)
    np.savetxt(filenames["polhemus_headshape_file"], polhemus_headshape)

copy_polhemus_files(recon_dir, subjects[0], [], [], [])

'''
We can now call the delete_headshape_points function we have defined above. 
Note that we can call this in two different ways, either:

1) Specify the subjects_dir AND the subject directory, in the directory structure used by RHINO: delete_headshape_points(recon_dir=recon_dir, subject=subject)
2) Specify the full path to the .npy file containing the (3 x num_headshapepoints) numpy array of headshape points: delete_headshape_points(polhemus_headshape_file=polhemus_headshape_file)

Here, we want to use the first option. Let's now call the function we defined above:
'''

polhemus.delete_headshape_points(recon_dir, subjects[0])
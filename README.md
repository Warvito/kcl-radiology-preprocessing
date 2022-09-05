# KCL Radiology - Preprocessing pipeline 

Originally defined on the Clinical clip project (https://github.com/Warvito/clinical_clip).


## Building Instructions
To build the Docker image locally, use:
```shell script
docker build -t kcl-radiology-preproc . \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  --build-arg USER=${USER}
```

## List of ids file (JSON file)
To be able to preprocess the data, it is necessary a JSON file containing the participants id and their 
relative path to the mounted ```/data/``` directory. For example, if I have my data inside the ```/my_local_data_root/``` dir
my json file should look like

```
{
  "participants": [
    {
      "participant_id": "sub-0001",
      "ses_id": "ses-01",
      "image_paths": [
        "/data/sub-0001/ses-01/anat/sub-0001_ses-01_T1w.nii",
        "/data/sub-0001/ses-01/anat/sub-0001_ses-01_T2w.nii",
        "/data/sub-0001/ses-01/anat/sub-0001_ses-01_FLAIR.nii"
      ]
    },
    {
      "participant_id": "sub-0002",
      "ses_id": "ses-20220808",
      "image_paths": [
        "/data/sub-0002/0002_T2w.nii",
        "/data/sub-0002/0002_T1w.nii"
      ]
    },
    {
      "participant_id": "sub-0003",
      "ses_id": "ses-01",
      "image_paths": [
        "/data/sub-0003/ses-01/anat/0003_ses-01_T2w.nii",
        "/data/sub-0003/ses-01/anat/0003_ses-01_T1w.nii"
      ]
    },
    ...
  ]
}
```
The "participant_id" and "ses_id" fields are used only to create the output directories

## Executing preprocessing
To execute preprocessing, use:
```shell script
nvidia-docker run \
    --volume /local_path_to_where_data_is_stored/:/data/ \
    --volume /local_path_to_where_save_preprocessed_data/:/target/ \
    --volume /local_path_to_dir_with_json_file/ids_dir/:/ids_dir/ \
    --user $(id -u):$(id -g) \
    -it  kcl-radiology-preproc \
      --ids_filename "/ids_dir/ids.json" \
      --pipeline_name "kcl_preprocessing" \
      --start 0 \
      --stop 5 
```

For example:
```shell script
nvidia-docker run \
    --volume /media/walter/Storage/Downloads/TEST/my_data/:/data/ \
    --volume /media/walter/Storage/Downloads/TEST/target/:/target/ \
    --volume /media/walter/Storage/Downloads/TEST/ids_dir/:/ids_dir/ \
    --user $(id -u):$(id -g) \
    -it  kcl-radiology-preproc \
      --ids_filename "/ids_dir/ids.json" \
      --pipeline_name "kcl_preprocessing" \
      --start 0 \
      --stop 5 
```

If your docker version have access to GPU, replace the ```nvidia-docker``` command with ```docker```.
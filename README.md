# DL_project_24_HR_GS
This is the submission repository of the course "Advanced Deep Learning Programming" ([Jakob Schwalb-Willmann](https://github.com/16EAGLE), summer semester 2024, "04-GEO-MET4") of the [EAGLE M.Sc.](https://eagle-science.org/) by Henning Riecken (henning.riecken@stud-mail.uni-wuerzburg.de) &amp; Georg Starz (georg.starz@stud-mail.uni-wuerzburg.de). 
The aim of this project was to identify construction / crane sites on high resolution orthophotos in Germany. 
This repo contains the scripts and results of the performed [YOLOv8](https://docs.ultralytics.com/) trainings. 
The construction sites GPKGs, labelled training images, and the trained models can be retrieved via the Drive folder link that was sent with the submission.

&nbsp;

![thumbnail](https://github.com/user-attachments/assets/ab96911a-0854-4931-a94a-31eb97c38c27)

&nbsp;

## Repo Overview 

For a detailed overview of the whole process of this project, please have a look into [presentation_UPDATED.pptx](https://github.com/Geo-99/DL_project_24_HR_GS/blob/main/presentation_UPDATED.pptx). 

Folder Structure:
- [0_data_preprocessing](https://github.com/Geo-99/DL_project_24_HR_GS/tree/main/0_data_preprocessing) contains the scripts to create .png files from point coordinates to then create training data for the models, and to augment (rotation) and split the images into training/validation/test (only relevant for cls training data - obb labelling and augmentation was done with Roboflow)   
- [1_obb_attempt](https://github.com/Geo-99/DL_project_24_HR_GS/tree/main/1_obb_attempt) contains relevant files of our approaches to build Oriented Bounding Box models on the basis of the YOLOv8-obb model 
  - "training_script" contains the google colab script to train the respective obb models & the .yaml file which stores the model parameters
  - "attempt_1/train" contains the results of the l model training (batch size = 1, epochs = 50), while "attempt_2/train" contains the results of the n model training (batch size = 8, epochs = 50)
  - "predict_script" contains the python script to run the models.
- [2_cls](https://github.com/Geo-99/DL_project_24_HR_GS/tree/main/2_cls) contains the results of 2 classification model trainings (m, l) on the basis of the YOLOv8-cls model and follows the same structure: 
  - "training_script" contains the colab script to train the models
  - "1_m_model" contains the results of the m model (batch size = 150, epochs = 200),  while "2_l_model" contains the results of the l model (batch size = 145, epochs = 400)
  - "predict_save_stats" contains the colab script to run the model and save the output stats as .txt and .xlsx files.
    - "test_1" contains the output stats of the m & l model for the test data (which the model has mostly already seen in augmented versions) 
    - "test_2" contains the output stats of the m & l model for completely unseen data (newly created pngs of 3 classes (no_constr, constr_without_crane, constr_with_crane)
    - The motivation behind the "test_2" was to check whether the model performs worse on images which it hasn't even seen in augmented form and to check the importance of construction cranes for the model classification.
- [3_rollout_berlin](https://github.com/Geo-99/DL_project_24_HR_GS/tree/main/3_rollout_berlin) contains python/colab scripts to run our cls model(s) over the whole DOP20 of Berlin
  - "1_creating_framework_points.py" to create a framework of points over the whole area of Berlin 
  - "2_rollout.ipynb" to create the image tiles based on the framework, run our cls model(s) over all the images and save the results (session timeouts due to computational time - can only be done in parts per session) 
  - "3_merging_rollout_parts.py" to merge the single parts (due to session timeouts in "2_rollout.ipynb") to get a complete result of Berlin ("merged_tiles.gpkg", "merged_points.gpkg").

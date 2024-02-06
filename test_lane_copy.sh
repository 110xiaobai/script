cd /mnt/script/ 
export LD_LIBRARY_PATH=/mnt/release:$LD_LIBRARY_PATH 
/mnt/release/acquire_fusion_bev \
/mnt/pco/20240117-144340_jing-PSA003/data/parse/20240117-144340_jing-PSA003/cam1_img_perception_info.json 
/mnt/pco/20240117-144340_jing-PSA003/data/parse/20240117-144340_jing-PSA003/perception_image_fov120/ 
/mnt/camera_parameters/JING_P_SA003_20230808/cam1_params.yml 
/mnt/pco/20240117-144340_jing-PSA003/data/parse/20240117-144340_jing-PSA003/cam2_img_perception_info.json 
/mnt/pco/20240117-144340_jing-PSA003/data/parse/20240117-144340_jing-PSA003/perception_image_fov30/ 
/mnt/camera_parameters/JING_P_SA003_20230808/cam0_params.yml 
log/bev_result.txt 
/mnt/pco/20240117-144340_jing-PSA003/20240117-144340_jing-PSA003 
none
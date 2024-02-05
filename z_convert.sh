pgbag_path=/mnt/pgbag2.0/pgbag2.0
export LD_LIBRARY_PATH=${pgbag_path}/lib:${pgbag_path}/third_party/lib:$LD_LIBRARY_PATH
cd ${pgbag_path}/bin


CIXI_DIR=/mnt/pco/20240117-144340_jing-PSA003
# CIXI_DIR=/mnt/data1/can.jin/data/bevlane_test/ningbogaojia/pco


for pack_file in `ls ${CIXI_DIR}`
# for pack_file in 20231207-153354.pco 20231207-153655.pco 20231207-153956.pco 20231207-154257.pco 20231207-154558.pco 20231207-154859.pco 20231207-155200.pco 20231207-155501.pco 
do
    echo "${CIXI_DIR}/${pack_file} start."
    # ./pgbag convert -f ${CIXI_DIR}/${pack_file} 
    ./pgbag info -f ${CIXI_DIR}/${pack_file} 
    ./pgbag parse -f ${CIXI_DIR}/${pack_file} 
    echo "${CIXI_DIR}/${pack_file} done."
done

echo "start move"
mv data $CIXI_DIR
echo "move done"


# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/20230911_case/pack
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/hmi_0815/data
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/20230915_case/pack
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/hmi_1012/pack
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/psd1.0_20231029/pack
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/psd1.0_20231106/pack
# python3 tools/generate_perception_from_pco_psd2.0.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20231114
# python3 tools/generate_perception_from_pco_psd2.0.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20231116
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/psd1.0_20231115/pack
# python3 tools/generate_perception_from_pack.py --pack_root=/mnt/data1/can.jin/data/pack/psd1.0_20231031/pack
# python3 tools/generate_perception_from_pco_psd2.0.py --pack_root=/mnt/data1/can.jin/data/pack/zxk_20231129
# python3 tools/generate_perception_from_pco_psd2.0.py --pack_root=/mnt/data1/can.jin/data/pack/hmi_20231130
# python3 tools/generate_perception_from_pco_perception_3d.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20231229
# python3 tools/generate_perception_from_pco_perception_3d.py --pack_root=/mnt/data1/can.jin/data/pack/byd_20231227
# python3 tools/generate_perception_from_pco_perception_3d_psd-v2.2.2.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20231228
# python3 tools/generate_perception_from_pco_perception_3d_psd-v2.2.2.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20231227
# python3 tools/generate_perception_from_pco_perception_3d.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20231219
# python3 tools/generate_perception_from_pco_perception_3d.py --pack_root=/mnt/data1/can.jin/data/pack/byd_20231227
# python3 tools/generate_perception_from_pco_perception_3d_psd-v2.2.2.py --pack_root=/mnt/data1/can.jin/data/pack/psd2.0_20240104

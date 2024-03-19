import os
import numpy as np
import json
from functools import cmp_to_key


def cmp(x,y):
    a=float(x.split(".")[0].split("_")[-1])
    b=float(y.split(".")[0].split("_")[-1])
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1
    
def cmp2(x,y):
    a=float(x.split(".")[0].split("_")[-2])
    b=float(y.split(".")[0].split("_")[-2])
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1
    
lanemark_type_list={
                    2:0,
                    1:5,
                    3:1,
                    0:0,
}


def parser_dynamic_6v(dynamic_6v_res,cam_id):
    lanes_res = []
    for cam_data in dynamic_6v_res['frameInfo_ptr']:
        if int(cam_data['camera_id'])!=cam_id:
            continue
        timestamp_ms = int(cam_data['timestamp'])
        lane_num = cam_data['lane_num']+cam_data['stop_lane_num']
        lanes_res.append(str(lane_num))
        lane_data = cam_data['lanes']
        for lane in lane_data:
            lane_res = []
            lane_res.append(int(lane['is_road_edge']))
            # is_stopline
            lane_res.append(int(False))
            lane_res.append(lane['score'])
            if int(lane['is_road_edge']):
                lane_res.append(1)
            else:
                lane_res.append(lane['color'])
            if lane['lanemark_type'] in lanemark_type_list.keys():
                lane_res.append(lanemark_type_list[lane['lanemark_type']])
            else:
                lane_res.append(0)
            coords = lane['coords']
            lane_res.append(len(coords))
            for pt in coords:
                lane_res.append(pt['x'])
                lane_res.append(pt['y'])
                lane_res.append(pt['score'])
            lane_res = map(str,lane_res)
            lane_txt = ' '.join(lane_res)
            lanes_res.append(lane_txt)

        lane_data = cam_data['stop_lanes']
        for lane in lane_data:
            lane_res = []
            lane_res.append(int(False))
            # is_stopline
            lane_res.append(int(True))
            lane_res.append(lane['score'])
            lane_res.append(0)
            if lane['lanemark_type'] in lanemark_type_list.keys():
                lane_res.append(lanemark_type_list[lane['lanemark_type']])
            else:
                lane_res.append(0)
            coords = lane['coords']
            lane_res.append(len(coords))
            for pt in coords:
                lane_res.append(pt['x'])
                lane_res.append(pt['y'])
                lane_res.append(pt['score'])
            lane_res = map(str,lane_res)
            lane_txt = ' '.join(lane_res)
            lanes_res.append(lane_txt)
        lanes_txt = ' '.join(lanes_res)
        # print(lanes_txt)
        return lanes_txt,timestamp_ms
    

def parser_lane(dynamic_6v_res,cam_id, img_name, speed, img_time, yaw_rate):
    lanes_dict = dict()
    lanes_dict["image_name"]=img_name;
    lanes_dict["speed"]=speed;
    lanes_dict["timestamp"]=img_time;
    lanes_dict["yaw_rate"]=yaw_rate;
    for cam_data in dynamic_6v_res['frameInfo_ptr']:
        if int(cam_data['camera_id'])!=cam_id:
            continue
        lanes_dict["lane_info"]=[]
        lane_data = cam_data['lanes']
        for lane in lane_data:
            lane_dict = dict()
            lane_dict["is_road_edge"]=int(lane['is_road_edge'])
            lane_dict["is_stopline"]=int(False)
            lane_dict["lane_score"]=lane['score']
            if int(lane['is_road_edge']):
                lane_dict["lane_color"]=1
            else:
                lane_dict["lane_color"]=lane['color']
            if lane['lanemark_type'] in lanemark_type_list.keys():
                lane_dict["lanemark_type"]=lanemark_type_list[lane['lanemark_type']]
            else:
                lane_dict["lanemark_type"]=0
            coords = lane['coords']
            lane_dict["point_info"]=[]
            for pt in coords:
                pt_dict=dict()
                pt_dict['x']=pt['x']
                pt_dict['y']=pt['y']
                pt_dict['point_score']=pt['score']
                pt_dict['point_lanetype']=-1
                lane_dict["point_info"].append(pt_dict)
            lanes_dict["lane_info"].append(lane_dict)
        
        lane_data = cam_data['stop_lanes']
        for lane in lane_data:
            lane_dict = dict()
            lane_dict["is_road_edge"]=int(False)
            lane_dict["is_stopline"]=int(True)
            lane_dict["lane_score"]=lane['score']
            lane_dict["lane_color"]=0
            if lane['lanemark_type'] in lanemark_type_list.keys():
                lane_dict["lanemark_type"]=lanemark_type_list[lane['lanemark_type']]
            else:
                lane_dict["lanemark_type"]=0
            coords = lane['coords']
            lane_dict["point_info"]=[]
            for pt in coords:
                pt_dict=dict()
                pt_dict['x']=pt['x']
                pt_dict['y']=pt['y']
                pt_dict['point_score']=pt['score']
                pt_dict['point_lanetype']=-1
                lane_dict["point_info"].append(pt_dict)
            lanes_dict["lane_info"].append(lane_dict)
     
    return json.dumps(lanes_dict)

def generate_perception_txt(pack_root,pack_file,cam_list):
    pack_path = os.path.join(pack_root,pack_file)
    perception_2d_path = pack_path+'/perception_3d_fusiontopic/'
    local_pose_path = pack_path+'/local_pose_topic/'
    images_fov120_path= pack_path+'/perception_image_fov120/'
    images_fov30_path= pack_path+'/perception_image_fov30/'

    input_info = dict()
    input_info_json = dict()
    for cam_id in cam_list:
        input_info[cam_id] = open(pack_path+'/cam{}_img_perception_info.txt'.format(cam_id), 'w')
        input_info_json[cam_id] = open(pack_path+'/cam{}_img_perception_info.json'.format(cam_id), 'w')
    
    # 处理底盘
    chaiss_files=os.listdir(local_pose_path)
    chaiss_files=sorted(chaiss_files, key = cmp_to_key(cmp))
    chaiss_dict=dict()
    for i in chaiss_files:
        chaiss_file=json.load(open(os.path.join(local_pose_path,i), 'r'))
        timestamp_ms=int(chaiss_file['header']['timestamp_ms'])
        ego_speed = float(chaiss_file['linear_velocity']['x'])
        yaw_rate = float(chaiss_file['angular_velocity']['z'])
        chaiss_dict[timestamp_ms]=[timestamp_ms,ego_speed,yaw_rate]

    txt_list = dict()
    json_list = dict()
    for cam_id in cam_list:
        txt_list[cam_id]=[]
        json_list[cam_id]=[]

    chaiss_np = np.array(list(chaiss_dict.keys()))

    max_diff=30
    perception_2d_files = [x for x in os.listdir(perception_2d_path) if x.endswith('json')]
    perception_2d_files.sort()
    for i_path in perception_2d_files:
        perception_2d_file=json.load(open(os.path.join(perception_2d_path,i_path), 'r'))
        for cam_id in cam_list:
            sync_timestamp = int(perception_2d_file['header']['sync_timestamp_ms'])
            if cam_id==1:
                img_name = "perception_image_fov30_{}_1.jpg".format(sync_timestamp,cam_id)
                if not os.path.exists(images_fov30_path+img_name):
                    print(img_name, " miss")
                    # continue
                    # assert 0
            if cam_id==2:
                img_name = "perception_image_fov120_{}_2.jpg".format(sync_timestamp,cam_id) 
                if not os.path.exists(images_fov120_path+img_name):
                    print(img_name, " miss")
                    # continue
                    # assert 0
            lanes_res, img_timestamp=parser_dynamic_6v(perception_2d_file,cam_id)
            if abs(img_timestamp-sync_timestamp)>max_diff:
                max_diff = abs(img_timestamp-sync_timestamp)
                print("bad img aligned, max time diff: ", max_diff)
                print(i_path)
            time_delta_chaiss = np.abs(img_timestamp-chaiss_np)
            sort_index_chaiss = np.argmin(time_delta_chaiss)
            if time_delta_chaiss[sort_index_chaiss]>30:
                print("bad match, time diff: ", time_delta_chaiss[sort_index_chaiss])
                # assert 0
            timestamp_ms,speed,yaw_rate = chaiss_dict[int(chaiss_np[sort_index_chaiss])]
            new_line = img_name +' {} {} {} '.format(speed, timestamp_ms, yaw_rate)+ lanes_res
            new_line_json = parser_lane(perception_2d_file,cam_id, img_name, speed, timestamp_ms, yaw_rate)
            txt_list[cam_id].append(new_line)
            json_list[cam_id].append(new_line_json)

    for cam_id in cam_list:
        input_info[cam_id].write('\n'.join(txt_list[cam_id]))
        input_info_json[cam_id] .write('\n'.join(json_list[cam_id]))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='parser pack')
    parser.add_argument("--pack_root", default='/mnt/data1/can.jin/data/pack/psd2.0_20231228', type=str)
    args = parser.parse_args()
    pack_root= args.pack_root

    pack_root = pack_root+"/data/parse"
    pack_list = os.listdir(pack_root)
    cam_list=[1,2]
    for pack in pack_list:
        print('{} start.'.format(pack))
        generate_perception_txt(pack_root,pack,cam_list)
        print('{} done.'.format(pack))





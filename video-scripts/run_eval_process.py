import subprocess
import sys
import os
import yaml
import glob

ROOT_FOLDER =  os.getcwd()

def Video_DASH_prep ():

   command = "bash DASH_prep.sh"

   subprocess.call(command, shell=True)


def frame_cut (interval, video_name, folder):

   command = "bash cuts.sh {} {} {}".format(video_name, interval, folder)

   subprocess.call(command, shell=True)

def get_resolution(frame_qlt):
   if frame_qlt == 'h':
      return '720'

   elif frame_qlt == 'm':
      return '540'

   elif frame_qlt == 'l':
      return '360'

   return 'missed'


def create_result_frame_list(load_sim, video_name, folder):

   file_line = ""

   file_line_file = ""

   sim_nr = load_sim['Sim_Number']

   for frame in load_sim['Frames']:

      frame_qlt = frame.split('_')[1]
      frame_nr  = frame.split('_')[0]

      resolution = get_resolution(frame_qlt)

      if resolution != 'missed':
         file_line += "file '{}{}_src{}/{}_{}_src{}.mp4'\n".format(ROOT_FOLDER + folder.split('.')[1], video_name, resolution, frame_nr, video_name, resolution)

   if file_line != "":
      file_line_file = "{}FRAME-LIST/{}_{}.txt".format(folder, video_name, sim_nr)

   write_file = file(file_line_file, 'w')
   write_file.write(file_line)
   write_file.close()

   return file_line_file

def create_result_video(frame_list_file, video_name, sim_nr, folder):

   command = "ffmpeg -f concat -safe 0 -i {} -c copy {}{}_SIM-{}-output.mp4".format(frame_list_file, folder, video_name, sim_nr)

   subprocess.call(command, shell=True) 

def main():

   video_dict = {"BusyStreetScene":"./vid_1/", "CarsStoping":"./vid_2/"}

   sim_fails = []

   if not os.path.isdir("./vid_1/BusyStreetScene_src") and not os.path.isdir("./vid_2/CarsStoping_src"):
      Video_DASH_prep()

   for v in video_dict:

      video_name = v
      folder = video_dict[v]

      frame_cut("1", video_name, folder)

      sim_runs_folder = folder + "SIM-RUNS/*.yaml"

      for sim_file in glob.iglob(sim_runs_folder):

         file_sim = file(sim_file, 'r')
         load_sim = yaml.load(file_sim)
         file_sim.close()

         sim_nr = load_sim['Sim_Number']

         frame_list_file = create_result_frame_list(load_sim, video_name, folder)

         if frame_list_file != "":

            create_result_video(frame_list_file, video_name, sim_nr, folder)

         else:
            sim_fails.append(sim_nr)

   fails = file('sim-fails.log', 'w')
   yaml.dump(sim_fails, fails, default_flow_style=False)


if __name__ == '__main__':
   main()
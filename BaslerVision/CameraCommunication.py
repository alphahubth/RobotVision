from pypylon import pylon
import cv2
import os
import supervision as sv
import time
import numpy as np
from camera_config import *


class CameraProcessor:

    @staticmethod
    def detect_cameras():
        return pylon.TlFactory.GetInstance().EnumerateDevices()
    
    devices = detect_cameras()

    def __init__(self, device_ip, config_path):
        print(f"Try initiating camera: {device_ip}")
        self.camera, self.converter = self.init_camera(device_ip, config_path)
        print(f"Initiate Camera & Converter {self.camera}", device_ip) 
        self.frame_count = 0
        self.mem_pool = []


    def init_camera(self, device_ip, config_path):
    
        for device in CameraProcessor.devices:

            if str(device.GetIpAddress()) == str(device_ip):
                camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(device)) # break point
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                # load config
                # pylon.FeaturePersistence.Load(config_path, camera.GetNodeMap(), True)
                converter = pylon.ImageFormatConverter()
                converter.OutputPixelFormat = pylon.PixelType_BGR8packed
                converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

                camera.RetrieveResult(5000, pylon.TimeoutHandling_Return)

                return camera, converter


    def capture(self, grabResult):
        image = self.converter.Convert(grabResult)
        image = image.GetArray()
        grabResult.Release()
        return image
    
    def trig_capture(self, device_ip):

        frame = np.array([])
        try:

            grabResult = self.camera.RetrieveResult(100, pylon.TimeoutHandling_Return)

            print(f"{device_ip[-1]} Grabbing: {self.camera.IsGrabbing()}, Succeeded: {grabResult.GrabSucceeded()}")

            if (self.camera.IsGrabbing() and grabResult.GrabSucceeded() and grabResult.IsValid()):
                frame = self.capture(grabResult)
                grabResult.Release()

            else:
                print("grab failed! one more trig please")

        except:
            return frame
        else:
            return frame



    def one_capture(self):
        try:
            while self.camera.IsGrabbing():
                
                try:
                    grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                    print(grabResult.GrabSucceeded())
                except:
                    print("exception")
                    grabResult = None

                else:
                    if grabResult.GrabSucceeded():
                        frame = self.capture(grabResult)
                        print(frame.shape)
                        # grabResult.Release()
                        return frame
                finally:
                    if grabResult is not None:
                        grabResult.Release()

        except KeyboardInterrupt:  
            self.release_camera()


    def timing_capture(self, exposure_time=30, max_mempool=10):
        try:
            self.mem_pool = []
            while self.camera.IsGrabbing():

                grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_Return)

                if grabResult.GrabSucceeded():
                    frame = self.capture(grabResult)

                    if self.frame_count % exposure_time == 0: 
                        self.mem_pool.append(frame)

                    self.frame_count += 1

                    if (len(self.mem_pool) > max_mempool):
                        print("Finish with len(mem_pool): ", len(self.mem_pool))
                        return self.mem_pool

                grabResult.Release()

        except KeyboardInterrupt:  
            self.release_camera()

    def release_camera(self):
        self.camera.StopGrabbing()
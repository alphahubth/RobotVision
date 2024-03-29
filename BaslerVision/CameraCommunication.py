from pypylon import pylon
import cv2
import os
import supervision as sv


class CameraProcessor:

    def __init__(self, device_ip, config_path):
        self.camera, self.converter, self.grabStatus = self.init_camera(device_ip, config_path)
        print(f"Initiate Camera & Converter {self.camera}", device_ip) 
        self.frame_count = 0
        self.mem_pool = []

    def init_camera(self, device_ip, config_path):

        def detect_cameras():
            return pylon.TlFactory.GetInstance().EnumerateDevices()
    
        devices = detect_cameras()

        for device in devices:
            if device.GetIpAddress() == device_ip:
                camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(device))
                break

        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # load config
        pylon.FeaturePersistence.Load(config_path, camera.GetNodeMap(), True)
        

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        # print(f"Initiate Camera & Converter {device_id}")
        # try:
        grabStatus = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        # except:
        #     grabStatus = None
        # finally:
        #     if grabStatus is not None:
        #         grabStatus.Release()

        return camera, converter, grabStatus

    def capture(self, grabResult):
        image = self.converter.Convert(grabResult)
        image = image.GetArray()
        return image

    def one_capture(self):
        try:
            
            while self.camera.IsGrabbing():
                try:
                    grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                except:
                    grabResult = None
                else:
                    if grabResult.GrabSucceeded():
                        frame = self.capture(grabResult)
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

                grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

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

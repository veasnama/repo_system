import os
import tarfile
class ProcessTarGZFile():
    def __init__(self):
        self.tar_file = None
        self.tar = None
        self.target_file = [
            "zpool_list.out",
            "ldm_list.out",
            "ilomconfig_list_system-summary.out",
            "qlc_qaucli_-dm_all_general.out",
            "uname-a.out"
        ]
        print("constructor run")
    def set_file(self,file_p,tar):
        self.tar_file = file_p 
        self.tar = tar
        for m in self.tar_file:
            if os.path.basename(m.name) in self.target_file:
                try:
                    with tar.extractfile(m) as file:
                        data = file.read()
                        try:
                            text_data = data.decode('utf-8')
                            print(text_data)
                        except UnicodeDecodeError as e:
                            print(f"error: {e}")
                        
                except tarfile.TarError as e:
                    print(f"error: {e}")

    def ProcessData(self):
        print("Processing....")
            

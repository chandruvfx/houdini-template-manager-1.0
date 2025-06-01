import templates_restapi
import constant
from pprint import pprint
from shutil import copy2
from importlib  import reload
reload(templates_restapi)
reload(constant)
import os
import hou


class FileOps:

    def make_dirs(self, path):
        try:
            os.makedirs(path)
        except FileExistsError:
            print(f"{path} already file written")
    
    def copy(self, src_path, dest_path):
        copy2(src_path, dest_path)


class SnipOps:

    """ Snips operation writing and loading .snip files into houdini """
    def save(self, path):
        selected_nodes = hou.selectedNodes()
        parent = selected_nodes[0].parent()
        parent.saveItemsToFile(selected_nodes,path)



class Publish:

    def __init__(self,
                bundle_name: str = '',
                description: str = '',
                version: int = 0,
                artist: str = '',
                file_path: str = '',
                file_type: str = '',
                frame_start: int = 0,
                frame_end: int = 0,
                img_path: str = '',
                bundle_type_id: int = 0,
                bundle_list_id: int = 0,
                category_id: int = 0,
                context_id: int = 0,
                houdini_version_id: int = 0,
                frame_count: int = 0,
                user_selected_img_path: str ='',
                user_screen_shot_img_path: str = '',
                user_tags: set = set()
    ) -> None:
        self.bundle_name=bundle_name
        self.description=description
        self.version=version
        self.artist=artist
        self.file_path=file_path
        self.file_type=file_type
        self.frame_start=frame_start
        self.frame_end=frame_end
        self.img_path=img_path
        self.bundle_type_id=bundle_type_id
        self.bundle_list_id=bundle_list_id
        self.category_id=category_id
        self.context_id=context_id
        self.houdini_version_id=houdini_version_id
        self.frame_count=frame_count
        self.user_selected_img_path = user_selected_img_path
        self.user_screen_shot_img_path = user_screen_shot_img_path
        self.user_tags = user_tags

        # pprint({f"bundle_name:{bundle_name}",
        #         f"description:{description}",
        #         f"version:{version}",
        #         f"artist:{artist}",
        #         f"file_path:{file_path}",
        #         f"file_type:{file_type}",
        #         f"frame_start:{frame_start}",
        #         f"frame_end:{frame_end}",
        #         f"img_path:{img_path}",
        #         f"bundle_type_id:{bundle_type_id}",
        #         f"bundle_list_id:{bundle_list_id}",
        #         f"category_id:{category_id}",
        #         f"context_id:{context_id}",
        #         f"houdini_version_id:{houdini_version_id}",
        #         f"frame_count:{frame_count}"})

    def ops(self) -> None:
        """Doing different operations

        Making folders writing hip files and transfering image 
        sequence with proper name 
        """
        # Make Dirs 
        file_ops = FileOps()
        file_ops.make_dirs(self.file_path)
        file_ops.make_dirs(self.img_path)

        new_file_path = os.path.join(self.file_path, f"{self.bundle_name}{self.file_type}")

        #Copy Image from src to dest folder
        if self.bundle_type_id == 1: # Templates

            # Copy hip path to the destination folder 
            # from source folder
            self.dest_file_path = new_file_path
            file_ops.copy(hou.hipFile.path(), new_file_path)
            

            first_image = []
            counter = 1
            for files in os.listdir(self.user_selected_img_path):
                src_file = os.path.join(self.user_selected_img_path, files)
                dest_file = os.path.join(self.img_path, f"{self.bundle_name}_{str(counter).zfill(3)}.jpg")
                if counter == 1:
                    first_image.append(dest_file)
                file_ops.copy(src_file, dest_file)
                counter = counter + 1
            
            self.dest_img_path = first_image[0].replace(constant.TEMPLATE_BUNDLE_PATH, "\\media\\")
            

        if self.bundle_type_id == 2:
            # Have to correct this
            save_snip = SnipOps()
            save_snip.save(new_file_path)
            file_ops.copy(self.user_screen_shot_img_path, self.img_path)
            self.dest_file_path = new_file_path
            self.dest_img_path = self.user_screen_shot_img_path.replace(constant.TEMPLATE_BUNDLE_PATH, "\\media\\")


        
    def register_db(self):
        
        template_rest_api = templates_restapi.TemplatesRestApi()

        # Create bundles register in db
        bundle_id = template_rest_api.insert_bundle(
            self.bundle_name,
            self.description,
            self.version,
            self.artist,
            self.dest_file_path,
            self.file_type,
            self.frame_start,
            self.frame_end,
            self.dest_img_path,
            self.bundle_type_id,
            self.bundle_list_id,
            self.category_id,
            self.context_id,
            self.houdini_version_id,
            self.frame_count
        )
        

        # Create M-to_M table Entry with bundle_id and tag_id
        for tag in [i for i in template_rest_api.tags()][0]:
            for user_tag in self.user_tags:
                if tag[-1] == user_tag:
                    tag_id = tag[0]
                    template_rest_api.bundle_tag_mtom_relation(bundle_id, tag_id)

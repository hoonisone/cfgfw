# class DB_ReferHandler:
#     # db id로 참조된 recode의 config file 경로를 찾아 @file_cif로 참조 변경 수행행

#     def __init__(self,
#             work_db:DB
#         )->None:

#         self.work_db = work_db

#     def is_target(self, string:Optional[Hashable])->bool:
#         return isinstance(string, str) and string.startswith("@db_cfg:")

#     def get_config_file_path(self, string:str)->str|Path:
#         # config 참조 string에서 config_file_path를 반환환
#         type, address = string.split(":")
#         db_name:str = address.split("/")[0]
#         id = int(address.split("/")[1])

#         return self.work_db.get_record(id).config_file_path
    
#     def handle(self, x:dict)->dict:
#         return RecursiveContext.replace(
#             data = x,
#             is_target = lambda v, k, idx: self.is_target(v),
#             replacement = lambda v, k, idx: f"{FileConfig_ReferHandler.MARK}{self.get_config_file_path(v)}"
#         )

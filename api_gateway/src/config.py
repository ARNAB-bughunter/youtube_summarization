import yaml


class Config:
    @classmethod
    def set_config(cls):
        cls.corpus = cls.parse_yaml("./config/config.yaml")

    @classmethod
    def parse_yaml(cls, file: str) -> dict:
        """ Parse yaml file into dict """
        try:
            with open(file, 'r') as f:
                info = yaml.safe_load(f)
            return info
        except Exception as e:
            print(f"Unable to find file.......{file}")
            raise Exception from e
    
    @classmethod
    def get_corpus(cls, main_key, sub_key)->list:
        main_key = cls.corpus.get(main_key, {})
        return main_key.get(sub_key,"")
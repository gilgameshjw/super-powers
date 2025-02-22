import yaml


class Config:
    _instance = None  # Class-level variable to store the singleton instance

    def __new__(cls, config_path=None):
        """Ensure only one instance of Config is created."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Initialize the instance only once
            if config_path:
                with open(config_path, "r") as f:
                    cls._instance.config = yaml.safe_load(f)
                
                cls._instance.llm_providers = cls._instance.config["llm_providers"]
                cls._instance.report_types = cls._instance.config["report_types"]
                cls._instance.browsers = cls._instance.config["browsers"]
                cls._instance.translations = None    
                cls._instance.language = None
                cls._instance.llm = None
                cls._instance.browser_search = None
                cls._instance.researcher = None
        return cls._instance

    def set_browser_search(self, browser_name):
        self.browser_type = self.browsers[browser_name]
        self.browser_api_key = self.browsers[browser_name]["api_key"]
        self.browser_search = {
            "type": self.browser_type,
            "api_key": self.browser_api_key
        }

    def set_llm_provider(self, provider_name):
        self.llm_provider = self.llm_providers[provider_name]
        self.api_key = self.config["llm_providers"][provider_name]["api_key"]
        self.model_version = self.llm_provider["model_version"]
        self.llm = {
            "api_key": self.api_key,
            "model_version": self.model_version
        }

    def set_researcher(self):
        self.researcher = {
            "openai_api_key": self.llm["api_key"], 
            "tavily_api_key": self.browser_search["api_key"]
        }

    def set_pages_translations(self, language):
        print("set pages translations")
        self.language = language
        self.file_translations = self.config["translations"]["file_translations"]
        with open(self.file_translations, "r") as f:
            self.translations = yaml.safe_load(f)[language]

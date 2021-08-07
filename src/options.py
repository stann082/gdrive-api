class Options:

    def __init__(self, cli_args=[]):
        key_vals = self.__parse(cli_args)
        self.fields = self.__set_property(key_vals, 'fields', 'files(name,mimeType,size)')
        self.filter_by = self.__set_property(key_vals, 'filterBy', 'name')
        self.order_by = self.__set_property(key_vals, 'orderBy', None)
        self.query = self.__set_property(key_vals, 'query', None)
        self.total = self.__set_property(key_vals, 'total', '10')

        self.is_descending = any("desc" in f for f in cli_args)
        self.order_by_size = True if self.order_by == "size" else False
        self.fetch_all_files = True if self.total == "all" else False


    def __parse(self, cli_args):
        key_vals = {}

        for arg in cli_args:
            key_val = arg.split('=')
            if len(key_val) != 2:
                continue

            key_vals[key_val[0]] = key_val[1].split(' ')[0]

        return key_vals

    def __set_property(self, key_vals, option_name, default_value):
        if not option_name in key_vals:
            return default_value

        return key_vals[option_name] if option_name in key_vals else default_value

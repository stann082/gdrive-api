class Options:

    def __init__(self, cli_args=[]):
        if len(cli_args) == 0:
            self.are_defined = False
            return None

        key_vals = self.__parse(cli_args)
        self.fields = key_vals['fields'] if 'fields' in key_vals else 'files(name,mimeType,size)'
        self.filter_by = key_vals['filterBy'] if 'filterBy' in key_vals else 'name'
        self.is_descending = any("desc" in f for f in cli_args)
        self.order_by = key_vals['orderBy'] if 'orderBy' in key_vals else None
        self.order_by_size = True if self.order_by == "size" else False
        self.query = key_vals['query'] if 'query' in key_vals else None
        self.total = key_vals['total'] if 'total' in key_vals else '10'
        self.fetch_all_files = True if self.total == "all" else False
        self.are_defined = True

    def __parse(self, cli_args):
        key_vals = {}

        for arg in cli_args:
            key_val = arg.split('=')
            if len(key_val) != 2:
                continue

            key_vals[key_val[0]] = key_val[1].split(' ')[0]

        return key_vals

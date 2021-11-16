def query_string_decoder(string, term, typeof, default):
    """Function to parse a string for a particular term and return the provided default if it cant find it"""
    try:
        var = [s for s in string.decode('utf-8').split('&') if term in s][0].split('=')[1]
        if typeof == 'string':
            var = str(var)
        elif typeof == 'int':
            var = int(var)
        elif typeof == 'bool':
            if var == 'False' or var == 'false':
                return False
            elif var == 'True' or var == 'true':
                return True
            else:
                pass
        else:
            parsed = {}
            for i in var.replace('--', '=').split(','):
                if i != '':
                    parsed[i.split('=')[0]]=i.split('=')[1]
            var = parsed
    except:
        var = default

    return var
